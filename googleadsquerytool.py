from google.ads.googleads.client import GoogleAdsClient
import pandas as pd
from google.ads.googleads.errors import GoogleAdsException
import sys
from re import match

class GoogleAdsDataFetcher:
    def __init__(self, customer_id):
        self.customer_id = customer_id.replace('-', '')
        self.client = GoogleAdsClient.load_from_storage()
        self.ga_service = self.client.get_service("GoogleAdsService")

    def fetch_data(self, query):
        search_request = self.client.get_type("SearchGoogleAdsStreamRequest")
        search_request.customer_id = self.customer_id
        search_request.query = query
        response = self.ga_service.search_stream(search_request)
        return response

class GoogleAdsQueryBuilder:
    def generate_query(self, select, from_resource_name, start_date=None, end_date=None, where=None, remove_zero_impressions=True):
        fields = ",\n".join(select.keys())
        statement = f"""
        SELECT \n{fields} 
        FROM 
            {from_resource_name}
        """
        # Construct WHERE clause
        if where:
            statement += f"""
            WHERE 
                {where}
            """
        # Check if WHERE clause is already present in the statement
        where_present = 'WHERE' in statement

        # Add filter for removing zero impressions
        if remove_zero_impressions:
            if 'WHERE' in statement:
                statement += """
                AND 
                    metrics.impressions > 0
                """
            else:
                statement += """
                WHERE 
                    metrics.impressions > 0
                """
        # Add date range filters
        if start_date:
            if 'WHERE' in statement:
                statement += f"""
                AND 
                    segments.date >= '{start_date}'
                """
            else:
                statement += f"""
                WHERE 
                    segments.date >= '{start_date}'
                """
        if end_date:
            if 'WHERE' in statement:
                statement += f"""
                AND 
                    segments.date <= '{end_date}'
                """
            else:
                statement += f"""
                WHERE 
                    segments.date <= '{end_date}'
                """
        return statement

class GoogleAdsDataProcessor:
    def process_response(self, response, attributes, headers = None):
        data = create_dict(attributes)
        for batch in response:
            for row in batch.results:
                for key in attributes.keys():
                    data[key].append(self.extract_data(row, key))
        df = pd.DataFrame(data)
        if headers:
            df.columns = headers
        return df

    def extract_data(self, row, key):
        # Extract data from the row based on the key
        data = row
        for sub_key in key.split('.'):
            data = getattr(data, sub_key)
        # If the key indicates a micros value, convert it to a regular number
        if match(pattern='.*(_micros)$|.*(cost).*|.*(_cpa)$', string=key):
            data /= 1e6
        return data

class GoogleAdsDataRetriever:
    def __init__(self, customer_id):
        self.data_fetcher = GoogleAdsDataFetcher(customer_id)
        self.query_builder = GoogleAdsQueryBuilder()
        self.data_processor = GoogleAdsDataProcessor()

    def get_data(self, query_fields, headers, from_resource_name, start_date=None, end_date=None, where=None, remove_zero_impressions=True):
        query = self.query_builder.generate_query(query_fields, from_resource_name, start_date, end_date, where, remove_zero_impressions)
        response = self.data_fetcher.fetch_data(query)
        data = self.data_processor.process_response(response, query_fields, headers=headers)
        return data

def create_dict(input_list):
    return {key: [] for key in input_list}
