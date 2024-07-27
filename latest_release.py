import os
import requests
from dotenv import load_dotenv


def get_releases_from_repo():
	"""
	This is used to get the details of latest release available in a repo
	:return:
	"""
	release_list = []
	github_repository = os.getenv('GITHUB_REPOSITORY')
	api_url = f'https://api.github.com/repos/{github_repository}/releases'
	per_page = 2
	page = 1
	headers = {
		'Accept' : 'application/vnd.github+json',
		'Authorization': f'Bearer {os.getenv("GH_TOKEN")}',
		'X-GitHub-Api-Version': '2022-11-28'
	}
	params = {'per_page': per_page, 'page': page}

	while True:
		response = requests.get(url=api_url, headers=headers, params=params)
		if response.status_code == 200:
			response_json = response.json()
			if not response_json:
				break
			release_list.extend(response_json)
			params['page'] += 1
		else:
			print('Faled to fetch details')
			break
	return release_list


def get_latest_release_from_repo():
	"""
	Get the latest release from repo
	:return:
	"""
	github_repository = os.getenv('GITHUB_REPOSITORY')
	api_url = f'https://api.github.com/repos/{github_repository}/releases/latest'

	headers = {
		'Accept': 'application/vnd.github+json',
		'Authorization': f'Bearer {os.getenv("GH_TOKEN")}',
		'X-GitHub-Api-Version': '2022-11-28'
	}
	response = requests.get(url=api_url, headers=headers)
	if response.status_code == 200:
		print(f'Data retrieved successfully from {github_repository}')
		response_json = response.json()
		# print(response_json)
		latest_release_tag = response_json['tag_name']
		print(f'Latest release tag on {github_repository} is {latest_release_tag}')

	return latest_release_tag



def main():
	"""To run code"""
	load_dotenv()
	# release_list = get_releases_from_repo()
	latest_release_tag = get_latest_release_from_repo()

if __name__ == "__main__":
	main()