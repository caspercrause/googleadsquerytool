# GoogleAdsQueryTool [![Latest Version](https://img.shields.io/badge/pypi-0.1.6-blue?&link=https%3A%2F%2Fpypi.org%2Fproject%2Fgoogleadsquerytool%2F)](https://pypi.org/project/googleadsquerytool/)

This is a package you can use to query reporting data from the Google Ads API.

## Build status
![Build Status](https://img.shields.io/badge/build-passing-brightgreen?label=build&color=lime)

## Requirements
 - Python 3.8+

## Installation
```
pip install googleadsquerytool
```
## Features
 - Distributed via PyPI.
 - Wrapper around the Google Ads API for easy reporting.
 - Returns data in the form of a pandas DataFrame.

 ## Example usage
 Before installing the library, you will need a developer token and client customer ID. Instructions on how to obtain them are outlined [here](https://developers.google.com/google-ads/api/docs/get-started/introduction). After you have successfully obtained your developer token and have successfully [authenticated](https://developers.google.com/google-ads/api/docs/oauth/overview) as per these instructions you need to create a `.yaml` file ([example](https://github.com/googleads/google-ads-python/blob/main/google-ads.yaml)) and place it in the home directory of your computer or virtual private server.

 ```
from googleadsquerytool import create_dict, GoogleAdsDataRetriever

# These represent your SELECT fields for a GAQL query:
fields = ['campaign.name', 'metrics.impressions', 'metrics.cost_micros', 'metrics.clicks']

# This represents the FROM portion of your GAQL query:
resource_name = 'campaign'

# Additional where clauses can be passed but are not mandatory
custom_where_clause = 'campaign.status = "ENABLED" AND campaign.serving_status = "SERVING"'

# Dictionary to append rows into:
ads_data = create_dict(fields)

# Create client object:
client = GoogleAdsDataRetriever(customer_id='Customer_id_that_your_mcc_account_has_access_to')

# Make a request to the API:
google_ads_data_df = client.get_data(
    query_fields=ads_data, 
    from_resource_name=resource_name, 
    headers=False, # Pass a list of headers that you would like to have
    start_date='2024-01-01',
    end_date='2024-01-31', 
    where=custom_where_clause, 
    remove_zero_impressions=True)
 ```

 For some queries, such as those involving campaign labels, start and end dates cannot be specified, nor can zero-impression rows be removed. In these cases, you can leave these fields blank.

 ```
fields = ['campaign.name', 'label.name', 'label.status', 'label.text_label.background_color']

resource_name = 'campaign_label'

label_data = create_dict(fields)

Header_names = ['Campaign', 'Label', 'Label Status', 'Label Color']

label_df = client.get_data(
    query_fields=label_data,
    from_resource_name=resource_name,
    headers=Header_names,
    remove_zero_impressions=False)
 ```