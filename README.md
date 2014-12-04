# pyalma
-------------------

## Setup

The Alma API requires a secret API key. You must also point to correct regional endpoint, of which there are three:

1. US: https://api-na.hosted.exlibrisgroup.com
2. EU: https://api-eu.hosted.exlibrisgroup.com
3. APAC: https://api-ap.hosted.exlibrisgroup.com

You can pass the key and region directly to the Alma object at the time of creation, like so:

    api = alma.Alma(apikey='xxxxxxxxxx', region='US')

Or, you can create environment variables in your operating system and the Python client will find it. On a linux machine you can do this by editing the `/etc/environment` file, like so:

    ALMA_API_KEY=xxxxxxxxx
    ALMA_API_REGION=US

After editing the `/etc/environment` file, be sure to reload it, like so:

    :$ source /etc/environment