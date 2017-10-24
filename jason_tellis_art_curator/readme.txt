Dear Dr. Khuri,
Please find below files to be run for the individual sections of the Assignment

BaseLine Performance

1. For image classifier:
   Main.py

   Please enter parameters as per user prompt.
   Either a single image or a directory of iamges can be provided

   I have used Manhattan Distance as Distance Metric
   And normalized histogram of bands of 16 values each to get an image vector with 48 values


Good Performance

1. For K-Fold Cross Validation of Headshots & Landscapes:
    CrossValidator.py

    Please provide a max value of 'K' as per user prompt, default will be 10. My dataset has 102 images so any number upto that count should be fine
    Output will be a box&whiskers plot
    Have ensured random selection of points and maintaining the proportion of images of each class in each fold based on their proportion
    in  original dataset


2. For K-Means Clustering of Headshots & Landscapes:
    KMeansClusteringEnvironment.py

    No input needed
    Will output a list of clusters

3. For Single Link Clustering of Headshots & Landscapes:
    HierarchicalClusteringEnvironment.py

    Will output clusters at a level
    Implemented logic to output clusters at any level

4. For Single Link Clustering of Flags
    FlagClusteringEnvironment.py

    Same as above

Excellent:
1. Could not implement GA for transformation
