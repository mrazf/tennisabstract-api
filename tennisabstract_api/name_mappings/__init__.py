from flask import Blueprint, jsonify, abort
import boto3

api = Blueprint('name_mappings', __name__)
dynamodb = boto3.client('dynamodb')

@api.route('/nameMappings')
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


@api.route('/nameMappings/<name>')
def name_mapping(name):
    mapping = dynamodb.get_item(TableName='Players', Key={ 'Name': {'S': str(name)} })
    if 'Item' not in mapping:
        abort(404)

    return jsonify(normalise_mapping(mapping['Item']))
