import os
import requests
import re
import argparse
import sys
from dotenv import load_dotenv
from latest_release import get_latest_release_from_repo
from get_label_from_pr import get_labels_of_a_pull_request, get_details_from_pull_request


def generate_major_release_tag(major: str):
	"""
	generate tag of sort vx.y.z in case of major update with label major
	:param major:
	:return:
	"""
	minor = 0 # reset minor to zero
	patch = 0 # reset patch to zero
	new_major = int(major)+1 # increase major by 1

	new_tag = f'v{new_major}.{minor}.{patch}'
	return new_tag


def generate_minor_release_tag(major:str,minor: str):
	"""
	generate tag of sort vx.y.z in case of minor update with label minor
	:param major:
	:param minor:
	:return:
	"""
	new_minor = int(minor) + 1 # increase minor by 1
	patch = 0 # reset patch to zero
	major = major

	new_tag = f'v{major}.{new_minor}.{patch}'
	return new_tag


def generate_patch_release_tag(major:str,minor: str, patch:str):
	"""
	generate tag of sort vx.y.z in case of patch update with label patch
	:param major:
	:param minor
	:param patch
	:return:
	"""
	minor = minor # stays same
	new_patch = int(patch) + 1 # increase patch by 1
	major = major # stays same

	new_tag = f'v{major}.{minor}.{new_patch}'
	return new_tag


def split_latest_release_into_components(latest_release: str):
	"""
	Split the latest release tag into its major minor patch components usingre gular expression
	:param latest_tag:
	:return:
	"""
	pattern = r'^v?(\d+)\.(\d+)\.(\d+)$'
	match = re.match(pattern, latest_release)
	if match:
		# major, minor, patch = match.groups()
		return match.groups()
	else:
		raise ValueError(f"Tag does not match the expected pattern of 3 semvar components {latest_release}.")


def process_previous_release_in_repository_and_get_new_release_tag(latest_release: str, pr_details: dict):
	"""
	process previous tag and generate new tag for release
	:return:
	"""
	major, minor, patch = split_latest_release_into_components(latest_release=latest_release)
	print(f'Tag components from latest release are - major:{major} minor:{minor} patch:{patch}')
	labels = pr_details['pull_request_labels']
	looking_for_labels = ['major', 'minor', 'patch']
	found_labels = [label for label in looking_for_labels if label in labels]
	if len(found_labels) > 1:
		print(f"More than 1 label found simultaneously. PR labels are  {labels} and expected ones are only one among {looking_for_labels}")
		sys.exit(1)
	elif not found_labels:
		print(f"No relevant label found in PR. Expected one among {looking_for_labels} But found {labels}")
		sys.exit(1)

	print(f"Found label : {found_labels[0]}")

	pr_label = found_labels[0] # zeroth index

	if pr_label == 'major':
		new_release_tag = generate_major_release_tag(major=major)
		print(f'Newer Release Tag will be {new_release_tag}')
	elif pr_label == 'minor':
		new_release_tag = generate_minor_release_tag(major=major, minor=minor)
		print(f'Newer Release Tag will be {new_release_tag}')
	else:
		new_release_tag = generate_patch_release_tag(major=major, minor=minor, patch=patch)
		print(f'Newer Release Tag will be {new_release_tag}')

	return new_release_tag


def create_new_release_github(new_release_tag: str, new_release_body: str, draft: bool, prerelease: bool, generate_release_notes:bool):
	"""
	create a new release in github repo using rest api
	:param new_release_tag:
	:return:
	"""
	github_repository = os.getenv('GITHUB_REPOSITORY')  # The owner and repository name
	api_url = f'https://api.github.com/repos/{github_repository}/releases'
	headers = {
		"Accept": "application/vnd.github+json",
		"Authorization": f"Bearer {os.getenv('GH_TOKEN')}",
		"X-GitHub-Api-Version": "2022-11-28"
	}
	data = {
		"tag_name": new_release_tag,
		"target_commitish": "main",
		"name": new_release_tag,
		"body": new_release_body,
		"draft": draft,
		"prerelease": prerelease,
		"generate_release_notes": generate_release_notes
	}
	response = requests.post(url=api_url, headers=headers, json=data)
	if response.status_code == 201:
		print(f"Release {new_release_tag} created successfully.")
	else:
		print(f"Failed to create release: {response.status_code}\n{response.text}")


def prepare_body_of_new_release(pull_request_details: dict):
	"""
	generate new release body to be passed to github rest api call
	:param pull_request_details:
	:return:
	"""
	title = pull_request_details['pull_request_title']
	pr_url =pull_request_details['pull_request_url']
	pr_opened_by = pull_request_details['pull_request_opened_by']
	pr_body = pull_request_details['pull_request_body']
	pr_created_at = pull_request_details['pull_request_created_at']
	pr_closed_at = pull_request_details['pull_request_closed_at']
	assignees_list = pull_request_details['pull_request_assignee']
	commits_no = pull_request_details['total_commits']
	merged = pull_request_details['pull_request_merged']

	assignees = ', '.join(assignees_list) if assignees_list else 'None'

	description = (
		f"**Pull Request Title**: {title}\n\n"
		f"**Pull Request URL**: [PR Link]({pr_url})\n\n"
		f"**Opened By**: {pr_opened_by}\n\n"
		f"**Merged**: {merged}\n\n"
		f"**Description**: {pr_body}\n\n"
		f"**Created At**: {pr_created_at}\n\n"
		f"**Closed & Merged At**: {pr_closed_at}\n\n"
		f"**Assignees**: {assignees}\n\n"
		f"**Total Commits**: {commits_no}\n"
	)

	return description

def eligible_for_a_release_from_pull_request(pull_request_details:dict):
	"""
	This fucntion checks whether the PR has been merged or not. if not merged not eligible to create a release
	:return:
	"""
	release_eligible = pull_request_details['pull_request_merged']
	return release_eligible


def main():
	"""to run code"""
	load_dotenv()
	parser = argparse.ArgumentParser("Arguments to create Github release action")
	parser.add_argument("--pr_number", help="Pull request number merged to main branch", type=int, required=True)
	parser.add_argument("--draft",default=False, help="To create a draft (unpublished) release", type=bool, required= False)
	parser.add_argument("--prerelease",default=False, help="true to identify the release as a prerelease. false to identify the release as a full release", type=bool, required=False)
	parser.add_argument("--generate_release_notes",default=False, help="Generate release notes", type=bool, required=False)

	args = parser.parse_args()
	pr_number = args.pr_number
	draft = args.draft
	prerelease = args.prerelease
	generate_release_notes = args.generate_release_notes

	latest_release = get_latest_release_from_repo()
	# latest_release = 'v1.2.9'
	pull_request_details = get_details_from_pull_request(pr_number=pr_number)
	release_eligible = eligible_for_a_release_from_pull_request(pull_request_details=pull_request_details)
	if release_eligible:
		print(f'PR {pull_request_details["pull_request_number"]} is merged')
		new_release_body = prepare_body_of_new_release(pull_request_details=pull_request_details)
		new_release_tag = process_previous_release_in_repository_and_get_new_release_tag(latest_release=latest_release, pr_details=pull_request_details)
		create_new_release_github(new_release_tag=new_release_tag, new_release_body=new_release_body, draft=draft, prerelease=prerelease, generate_release_notes=generate_release_notes)


if __name__ == "__main__":
	main()