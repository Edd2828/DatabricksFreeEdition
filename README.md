# Instructions to create bundle in databricks workspace:
This demo creates pipeline and dashboard in databricks via the databricks cli. It collects data from `https://restcountries.com/` and builds materialized views in a silver and gold layer following a kimbal model. The gold views are then used to suppliment the dashboard.

## Requirements
- Databricks CLI v0.242.1 or above
- python
- Databricks Free Edition Login

### 1. check profile is created
```cmd 
databricks auth profiles
```
### 2. login if profile is not created
```cmd
databricks auth login --host "https://{workspace}.cloud.databricks.com" -p [profile]
```
### 3. validate bundle
```cmd
databricks bundle validate -p [profile]
```
### 4. deploy bundle
```cmd
databricks bundle deploy -p geo
```