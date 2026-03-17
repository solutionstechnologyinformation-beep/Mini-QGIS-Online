#!/bin/bash

echo "Importando dados IBGE..."

ogr2ogr \
-f "PostgreSQL" \
PG:"dbname=gis user=gis password=gis" \
geodata/ibge/municipios.shp