[![Build Status](https://travis-ci.org/gri-is/pyalma.svg?branch=master)](https://travis-ci.org/gri-is/pyalma)

[![Coverage Status](https://coveralls.io/repos/github/gri-is/pyalma/badge.svg?branch=master)](https://coveralls.io/github/gri-is/pyalma?branch=master)

PyAlma
======

Developer Installation
----------------------

0. Ensure that Python 3 is installed on your machine (https://www.python.org/downloads/)

1. Create a directory for development projects on your machine
        
        $ mkdir /<path on your machine>/projects
        $ cd /<path>/projects

2. Clone the repository

        $ git clone https://<your login>@stash.getty.edu/scm/griis/pyalma.git
        $ cd pyalma

3. Create a virtual environment and activate it

        $ pyvenv ENV
        $ source ENV/bin/activate

4. Install dependencies to the virtual environment

        (ENV)$ pip install -r requirements.txt

5. Run the tests to make sure everything works correctly

        (ENV)$ python -m unittest

Developer Changes
-----------------

6. When working on a new issue, be sure to do so in a new branch

        (ENV)$ git branch <issue-name>
        (ENV)$ git checkout <issue-name>

7. Run a status check before doing any adds, commits or pushes

        (ENV)$ git status

8. Stage edited or newly created files

        (ENV)$ git status    
        (ENV)$ git add <name of file>

9. Commit the staged changes and ALWAYS explain the changes in a message

        (ENV)$ git status
        (ENV)$ git commit -m <message>

10. Push the changes to the shared repository, using the same branch name

        (ENV)$ git status
        (ENV)$ git push origin <issue-name>

11. On the repository website create a pull request from your branch to the master branch

12. When your branch has been reviewed, approved, and merged, you can pull the master and delete your issue branch

        (ENV)$ git checkout master
        (ENV)$ git status
        (ENV)$ git pull origin master
        (ENV)$ git branch -d <issue-name>


API KEY Configuration
---------------------

The Alma API requires a secret API key. You must also point to correct regional endpoint, of which there are three:

1. US: https://api-na.hosted.exlibrisgroup.com
2. EU: https://api-eu.hosted.exlibrisgroup.com
3. APAC: https://api-ap.hosted.exlibrisgroup.com

You can pass the key and region directly to the Alma object at the time of creation, like so:

    from pyalma.alma import Alma
    api = alma.Alma(apikey='xxxxxxxxxx', region='US')

Or, you can create environment variables in your operating system and the Python client will find it. On a linux machine you can do this by editing the `/etc/environment` file, like so:

    ALMA_API_KEY=xxxxxxxxx
    ALMA_API_REGION=US

After editing the `/etc/environment` file, be sure to reload it, like so:

    :$ source /etc/environment

For Mac OSX, this may be slightly different. This document may be of some help: http://www.dowdandassociates.com/blog/content/howto-set-an-environment-variable-in-mac-os-x-terminal-only/
