#!/bin/sh

for variable in `cat variables.tf | json2hcl -reverse | jq -rc '.variable[] | {_variable_name: . | keys[], _data: .[]} | select(._data[].description == null) | ._variable_name'`; do grep -E "^variable \"$variable\" {" -Rn; done

