
# Validation Results


  

## Overview
### **Expectation Suite:** **metoffice_historical_station_data**
 **Data asset:** **None**
 **Status:**  **Failed**





### Statistics


  
  
  

 |  |  |
 | ------------  | ------------ | 
Evaluated Expectations  | 22  
Successful Expectations  | 12  
Unsuccessful Expectations  | 10  
Success Percent  | ≈54.55%  








      
      
        

    ### Info


      
      
      

     |  |  |
     | ------------  | ------------ | 
    Great Expectations Version  | 0.18.15  
    Run Name  | 2024-05  
    Run Time  | 2024-06-09T17:08:37Z  


      
      
        

    ### Batch Markers


      
      
      

     |  |  |
     | ------------  | ------------ | 
    **ge_load_time**  | **20240609T160837.675721Z**  
    **pandas_data_fingerprint**  | **f2cabdd6a37aeeafec8fb568c03106cf**  


      
      
        

    ### Batch Spec


      
      
      

     |  |  |
     | ------------  | ------------ | 
    **batch_data**  | **PandasDataFrame**  





  

## af






  

 | Status | Expectation | Observed Value |
 | ------------  | ------------  | ------------ | 
✅  | is a required field.  | --  
❌  | values must never be null.

**2327** unexpected values found. **≈5.911%** of **39365** total rows.


  

 | Sampled Unexpected Values | Count |
 | ------------  | ------------ | 
null  | 20  
  | ≈94.089% not null  



  

## af_is_estimated






  

 | Status | Expectation | Observed Value |
 | ------------  | ------------  | ------------ | 
✅  | is a required field.  | --  
❌  | values must belong to this set: **False**.

**812** unexpected values found. **≈2.192%** of **39365** total rows.


  

 | Sampled Unexpected Values | Count |
 | ------------  | ------------ | 
True  | 20  
  | ≈2.1923% unexpected  



  

## month






  

 | Status | Expectation | Observed Value |
 | ------------  | ------------  | ------------ | 
✅  | is a required field.  | --  



  

## rain






  

 | Status | Expectation | Observed Value |
 | ------------  | ------------  | ------------ | 
✅  | is a required field.  | --  
❌  | values must never be null.

**873** unexpected values found. **≈2.218%** of **39365** total rows.


  

 | Sampled Unexpected Values | Count |
 | ------------  | ------------ | 
null  | 20  
  | ≈97.782% not null  



  

## rain_is_estimated






  

 | Status | Expectation | Observed Value |
 | ------------  | ------------  | ------------ | 
✅  | is a required field.  | --  
❌  | values must belong to this set: **False**.

**790** unexpected values found. **≈2.052%** of **39365** total rows.


  

 | Sampled Unexpected Values | Count |
 | ------------  | ------------ | 
True  | 20  
  | ≈2.0524% unexpected  



  

## station_name






  

 | Status | Expectation | Observed Value |
 | ------------  | ------------  | ------------ | 
✅  | is a required field.  | --  



  

## sun






  

 | Status | Expectation | Observed Value |
 | ------------  | ------------  | ------------ | 
✅  | is a required field.  | --  
❌  | values must never be null.

**9098** unexpected values found. **≈23.11%** of **39365** total rows.


  

 | Sampled Unexpected Values | Count |
 | ------------  | ------------ | 
null  | 20  
  | ≈76.888% not null  



  

## sun_is_estimated






  

 | Status | Expectation | Observed Value |
 | ------------  | ------------  | ------------ | 
✅  | is a required field.  | --  
❌  | values must belong to this set: **False**.

**1054** unexpected values found. **≈3.482%** of **39365** total rows.


  

 | Sampled Unexpected Values | Count |
 | ------------  | ------------ | 
True  | 20  
  | ≈3.4823% unexpected  



  

## tmax






  

 | Status | Expectation | Observed Value |
 | ------------  | ------------  | ------------ | 
✅  | is a required field.  | --  
❌  | values must never be null.

**928** unexpected values found. **≈2.357%** of **39365** total rows.


  

 | Sampled Unexpected Values | Count |
 | ------------  | ------------ | 
null  | 20  
  | ≈97.643% not null  



  

## tmax_is_estimated






  

 | Status | Expectation | Observed Value |
 | ------------  | ------------  | ------------ | 
✅  | is a required field.  | --  
❌  | values must belong to this set: **False**.

**886** unexpected values found. **≈2.305%** of **39365** total rows.


  

 | Sampled Unexpected Values | Count |
 | ------------  | ------------ | 
True  | 20  
  | ≈2.3051% unexpected  



  

## tmin






  

 | Status | Expectation | Observed Value |
 | ------------  | ------------  | ------------ | 
✅  | is a required field.  | --  
❌  | values must never be null.

**902** unexpected values found. **≈2.291%** of **39365** total rows.


  

 | Sampled Unexpected Values | Count |
 | ------------  | ------------ | 
null  | 20  
  | ≈97.709% not null  



  

## tmin_is_estimated






  

 | Status | Expectation | Observed Value |
 | ------------  | ------------  | ------------ | 
✅  | is a required field.  | --  
❌  | values must belong to this set: **False**.

**810** unexpected values found. **≈2.106%** of **39365** total rows.


  

 | Sampled Unexpected Values | Count |
 | ------------  | ------------ | 
True  | 20  
  | ≈2.1059% unexpected  




-----------------------------------------------------------
Powered by [Great Expectations](https://greatexpectations.io/)