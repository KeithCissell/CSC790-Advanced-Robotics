% set data directory
data_dir = fullfile('C:', 'home', 'keith', 'ros_workspaces', 'csc790_ws', 'in_class', '2018-4-23_segmentation', 'data', 'barrel_segmented');

% semantic class labels (string) and colors (rgb double: [0..1])
% (CamVid: http://mi.eng.cam.ac.uk/research/projects/VideoRec/CamVid/)
% - 1st element: foreground priority (1=low, 2=high)
% - 2nd element: rgb color [0..1]^3
% - 3rd element: textual description
labels = [];
labels{end+1} = {2, [255  165  0]/256, 'Barrel'};
labels{end+1} = {2, [255  165  0]/256, 'Cone'};

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% image / label / segment directories
image_dir = [data_dir '/images'];
label_dir = [data_dir '/labels'];
segment_dir = [data_dir '/segments'];
instance_dir = [data_dir '/instances'];

% create directories if they don't exist
if ~exist(image_dir,'dir'), mkdir(image_dir); end
if ~exist(label_dir,'dir'), mkdir(label_dir); end
if ~exist(segment_dir,'dir'), mkdir(segment_dir); end
if ~exist(instance_dir,'dir'), mkdir(instance_dir); end
