from flask import Blueprint, jsonify, abort
import boto3

name_mappings_api = Blueprint('name_mappings_api', __name__)
dynamodb = boto3.client('dynamodb', region_name='eu-west-1')

@name_mappings_api.route('/nameMappings')
def name_mappings():
    normalised = map(normalise_mapping, dynamodb.scan(TableName='Players')['Items'])

    return jsonify(nameMappings = normalised)


def normalise_mapping(mapping):
    return {
        mapping['Name']['S']: {
            'betfairName': mapping['BetfairName']['S'],
            'tennisAbstractName': mapping['TennisAbstractName']['S']
        }
    }


@name_mappings_api.route('/nameMappings/<name>')
def name_mapping(name):
    mapping = dynamodb.get_item(TableName='Players', Key={ 'Name': {'S': str(name)} })
    if 'Item' not in mapping:
        abort(404)

    return jsonify(normalise_mapping(mapping['Item']))
