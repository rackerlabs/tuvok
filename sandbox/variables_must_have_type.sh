#!/bin/sh

cat variables.tf | json2hcl -reverse | jq '.variable[] | {_variable_name: . | keys[], _data: .[]} | select(._data[].type == null) | "variable \(._variable_name) is missing type"'

