# devwithkrishna-create-release-action
An action to create release in GitHub

# What's New

Please refer to the [release](https://github.com/devwithkrishna/devwithkrishna-create-release-action/releases) page for the latest release notes.

# Input arguments

| Input name             | Description                                     | Required           | Default value    |
|------------------------|-------------------------------------------------|--------------------|------------------|
| token                  | GitHub access token                             | :heavy_cehck_mark: | No default value | 
| pr_number              | Pull request number triggered the workflow      | :heavy_cehck_mark: | No default value |
| draft                  | draft release or not. Boolean value             | ❌                  | Default - false |
| prerelease             | Release is latest or pre-release. Boolean value | ❌ | Default - false |
| generate_release_notes | Auto generate release notes. Boolean value      | ❌ | Default - false |

* Draft parameter and prerelease can not be used at same time. Either one can be used at a time.

* ❌ 👉 Means optional values

# General Usage 

```markdown
    - name: create-release
      uses: devwithkrishna/devwithkrishna-create-release-action@v1.0.0
      with:
        token: <your token reference here>
        pr_number: ${{ github.event.number }} #this will be passed from workflow 
        draft: true / false
        prerelease: true / false
        generate_release_notes: true / false
```

# How the releases are created
```shell
.
|-- Dockerfile
|-- LICENSE
|-- README.md
|-- action.yml
|-- create_new_release.py
|-- entrypoint.sh
|-- get_label_from_pr.py
|-- latest_release.py
|-- pyproject.toml
```

* This is specifically designed for Github usecase in which a Pull request is raised to merge a change from `Non main branch` to `main branch`

* Expects a Specific label in PR. label should be one among `first-release`, `major`, `minor`, `patch` (case sensitive). only one among these.

* When PR is merged to main branch and finds one among above lables, based on label it creates a new tag and generates the release

* The token provided should have sufficient previllage to create a tag and release.

* A PR should be merged to main branch to generate a release.

* You can have n number of labels on PR. But for this to work one from `first-release`, `major`, `minor`, `patch` should be present and only one.

* If the label `first-release` is found the release version will be `v1.0.0`. first release should only be used one time to create the first release version.

* If it finds `major` label, this will increase the major version by 1 and `resets patch and minor components`

* If it finds `minor` label, this will increase the minor version by 1 and `resets patch keeping major same`

* If it finds `patch` label, this will increase the patch version by 1 and `major and minor components are kept unchanged`

# Example usages

# Pass a secret as token for devwithkrishna/devwithkrishna-create-release-action 

```markdown
- name: create-release
      uses: devwithkrishna/devwithkrishna-create-release-action@v1.0.0
      with:
        token: ${{ secrets.TOKEN }}
        pr_number: ${{ github.event.number }} #this will be passed from workflow 
```
* Assuming you have a `token with name TOKEN` set in GITHUB SECRETS  

# Draft release creation

```markdown
- name: create-release
      uses: devwithkrishna/devwithkrishna-create-release-action@v1.0.0
      with:
        token: ${{ secrets.TOKEN }}
        pr_number: ${{ github.event.number }} #this will be passed from workflow 
        draft: true
```
* Assuming you have a `token with name TOKEN` set in GITHUB SECRETS

# Pre release with auto generate release notes

```markdown
    - name: create-release
      uses: devwithkrishna/devwithkrishna-create-release-action@v1.0.0
      with:
        token: ${{ secrets.TOKEN }}
        pr_number: ${{ github.event.number }}
        generate_release_notes: true
        prerelease: true
```
* Assuming you have a `token with name TOKEN` set in GITHUB SECRETS


# Pass a token generated from another action

```markdown
name: create release

on:
  pull_request:
    types:
    - closed
    branches:
    - main

jobs:
  create-release:
    runs-on: ubuntu-latest

    steps:

    - name: Token generator
      uses: githubofkrishnadhas/github-access-using-githubapp@v2
      id: token-generation
      with:
        github_app_id: ${{ secrets.APP_ID }}
        github_app_private_key : ${{ secrets.PRIVATE_KEY }}

    - name: create-release
      uses: devwithkrishna/devwithkrishna-create-release-action@v1.0.0
      with:
        token: ${{ steps.token-generation.outputs.token }}
        pr_number: ${{ github.event.number }}
        generate_release_notes: true
```
