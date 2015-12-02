### Tue Dec  1 21:03:23 CST 2015

##### Reason for change
Socrata's new backend does not provide cached contents.

##### Description
All code pertaining to ```cachedContents``` is deprecated and must be removed.  Data types, extreme values, null counts, etc. will have to be calculated for each column in each dataset individually.

##### Results of change
The following columns of output CSV files will be absent: ```num_null, num_not_null, ex_value```.
End users will not have information that was being gathered from the cached contents provided by Socrata unil we write code to fill those columns.
