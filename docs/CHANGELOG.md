###### Sun Dec 20 14:31:57 CST 2015
### Description
One script provides an interface to both static and online analysis, rather than having seperate scripts for each.

#### Reason for change
The portal analyzer should be easy to use and the interface should be simple.

#### Results of change
 The first major release (v1.0.0) marks the start of backward-compatability for this project.


###### Tue Dec  1 21:03:23 CST 2015
### Description
All code pertaining to ```cachedContents``` is deprecated and must be removed.  Data types, extreme values, null counts, etc. will have to be calculated for each column in each dataset individually.

#### Reason for change
Socrata's new backend does not provide cached contents.

#### Results of change
The following columns of output CSV files will be absent: ```num_null, num_not_null, ex_value```.
End users will not have information that was being gathered from the cached contents provided by Socrata unil we write code to fill those columns.
