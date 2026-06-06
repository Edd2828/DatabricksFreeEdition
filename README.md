# Instructions to create bundle in databricks workspace:
This demo creates a pipeline and dashboard in databricks via the databricks cli. It collects data from `https://restcountries.com/` and builds materialized views in a silver and gold layer following a kimbal model. The gold views are then used to build the dashboard.

## Requirements
- Databricks CLI v0.242.1 or above
- Databricks Free Edition Login

### 1. login if profile is not created
```cmd
databricks auth login --host "https://{workspace}.cloud.databricks.com" -p [profile]
```
### 2. check profile is created
```cmd 
databricks auth profiles
```
### 3. validate bundle
```cmd
databricks bundle validate -p [profile]
```
### 4. deploy bundle
```cmd
databricks bundle deploy -p geo
```
### 5. Run pipeline
Trigger the `geo_pipeline` under the `Jobs & Pipelines` tab in the databricks main page.
### 6. View Dashboard
Once the pipeline is finished running you will be able to view `Geo Summary` under the `Dashboards` tab.