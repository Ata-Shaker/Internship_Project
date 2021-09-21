Author: Ata Shaker

Email: atashaker13@gmail.com

--Ata's Image Editor--

On July 25, 2021, I started my Bachelor's Internship in Acoustic Sensing and Imaging Laboratory at Istanbul Technical University. During my tenure, I was tasked with building an application that crops and merges shorter images of seismic signals with equal length into one longer image. The application also can draw rectangular boxes on the final image and print comments under the boxes either by reading a CSV file with *.csv or *.txt extensions or  accepting single inputs by the user.

WARNING: BECAUSE OF USING ARIAL FONT OF THE WINDOWS FOR COMMENTS,  THE APPLICATION IS RUNNABLE ONLY ON WINDOWS. IF ANY FUTURE DEVELOPER COULD MODIFY THIS IN A WAY THAT THE APP IS INDEPENDENT FROM WINDOWS FONTS FOLDER, THE APP WITH HIGH PROBABILITY WILL BE RUNNABLE ON OTHER PLATFORMS TOO.

The whole application is written across three files. As the file names suggest, “Internship_Project_Main.py” delineates the General User Interface’s structure and is the file that start the application,  “Internship_Project_Ctrl.py” controls the general behavior of the application, and “Internship_Project_Dialog.py” contains the GUI of dialog window’s structure and how it functions. 

The user must gather all images that are to be merged into a single directory beforehand.
When the user runs the program a window with a fixed size will appear. To start, the user must select the directory containing the input images by clicking on the first browse button. Next the user must select the folder where the final image is to be saved using the second browse button and determine its name and extension using the input field and combobox below the browse buttons.

WARNING: DISCRETION IS ADVISED BEFORE SELECTING *.PNG AND *.JPEG AS SELECTING *.PNG FILE TYPE MIGHT RESULT IN LONGER IN RUN TIMES AND *.JPEG FILE TYPE HAS A RESTRICTIVE CONDITION ON THE DIMENSIONS OF THE FILE. THE *.JPEG OR *.JPG FILE TYPE PROHIBITS DIMENSIONS LONGER THAN 65535 PIXELS. 

In the next step, the user must either choose to proceed to create a new file or already annotate an existing one. Before merging on the “Merge” tab, the user can input the actual start time of the recording in the real world. Then the user can also select either 30, or 60, or 90, or 120 minutes as the time interval with which the record start time will be updated across the final image. 

After merging the user can continue to annotate on the “Annotate” tab. On the “Annotate” tab the user can add boxes one by one by filling the “Start Time” , “Finish Time” or “Time Length”, and selecting a color from the combo box, finally clicking on the “Annotate” button at the bottom. Adding a comment is voluntary. 

In case the user decides to add multiple boxes, they must create a *.CSV or a CSV-like *.TXT file containing the columns “Row”, “Start Time”, “End Time(True)/Time Length(False)” , “Bool”, “Comment” , “Color” otherwise there will be an error. The application is also capable of distinguishing between time length and endtime by reading the “End Time(True)/Time Length(False)” column. If the “End Time(True)/Time Length(False)” entry is one of the following: “True”, “T”, “1”, “Yes”, the application will interpret it as End Time. In case the entry is one of the following “False”, “F”, “0”, “No”, the application will interpret as Time Length. 

WARNING: WHILE ENTERING TIME DATA TO THE *.CSV OR *.TXT FILE, “HH:MM:SS” MUST BE FOLLOWED, OTHERWISE, THAT ROW WILL BE DISQUALIFIED FROM EVALUATING. ALSO, PROVIDING ENTRY WHICH IS NOT MENTIONED ABOVE TO THE  “End Time(True)/Time Length(False)” COLUMN WILL ALSO RESULT IN DISQUALIFICATION. 

The users are advised to select existing colors in the color combo box. In case the provided color doesn't exist in the color list or simply non-existent, the color blue will be chosen.

