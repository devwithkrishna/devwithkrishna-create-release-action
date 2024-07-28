import os
import requests
from dotenv import load_dotenv


def get_assignees_of_a_pull_request(assignees: list):
	"""
	Assignees on a PR can be upto 10 nos. getting the names of assignees corresponding to the PR
	:param assignees:
	:return:
	"""
	assignees_list = []
	for assignee in assignees:
		assignees_list.append(assignee['login'])

	return assignees_list


def get_labels_of_a_pull_request(labels: list):
	"""
	Labels on a PR can be multiple. getting the labels on a pr
	:param labels:
	:return:
	"""
	labels_list = []
	for label in labels:
		labels_list.append(label['name'])

	return labels_list


def get_details_from_pull_request(pr_number: int):
	"""
	get details from a PR in github
	:return:
	"""
	github_repository = os.getenv('GITHUB_REPOSITORY') # The owner and repository name
	pull: int = pr_number
	api_url = f'https://api.github.com/repos/{github_repository}/pulls/{pull}'
	headers = {
		"Accept": "application/vnd.github+json",
		"Authorization": f"Bearer {os.getenv('GH_TOKEN')}",
		"X-GitHub-Api-Version": "2022-11-28"
	}
	print(f'Retreving details from pull request #{pull} - {github_repository} repository')
	response = requests.get(url=api_url, headers=headers)
	if response.status_code == 200:
		print(f'Data retrieved from pull request #{pull} from {github_repository}')
		response_json = response.json()
		# print(response_json)
	elif response.status_code == 304:
		print(f'Not Modified')
	elif response.status_code == 404:
		print(f'Resource Not found')
	elif response.status_code == 406:
		print(f'Unacceptable')
	elif response.status_code == 500:
		print(f'internal server error')
	else:
		print('Service unavailable')
	pull_request_details = {'pull_request_title': response_json['title'], 'pull_request_url': response_json['url'],
							'pull_request_opened_by': response_json['user']['login'],
							'pull_request_body': response_json['body'],
							'pull_request_created_at': response_json['created_at'],
							'pull_request_closed_at': response_json['closed_at']}
	assignees_list = get_assignees_of_a_pull_request(response_json['assignees'])
	pull_request_details['pull_request_assignee'] = assignees_list
	labes_list = get_labels_of_a_pull_request(response_json['labels'])
	pull_request_details['pull_request_merged'] = response_json['merged']
	pull_request_details['pull_request_number'] = response_json['number']
	pull_request_details['pull_request_labels'] = labes_list
	pull_request_details['total_commits'] = response_json['commits']

	return pull_request_details


def main():
	"""To run the code"""
	load_dotenv()
	get_details_from_pull_request()



if __name__ =="__main__":
	main()