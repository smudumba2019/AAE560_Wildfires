%% In this MATLAB program, I try to present a geographical map of a region we are studying for AAE 560 project
% Author: Sai V. Mudumba
% Date: 03/30/2020
clear all;
%% Open files and import data
cd 'Border_Shapefile'
Borders_shp = shaperead('tl_2016_06_cousub.shp'); % this loads the border shapefile of California 
[~,index] = sortrows({Borders_shp.COUNTYFP}.'); Borders_shp = Borders_shp(index); clear index % this sorts the list based on the county codes (Butte County is 007)
Borders_shp = Borders_shp(12:19,:); % this selects all those regions that fall in 007 
cd ..
cd 'Roads'
Roads_shp = shaperead('tl_2013_06007_roads.shp'); % this loads the roads shapefile of Butte County, CA
cd ..
cd 'Water'
Water_shp = shaperead('tl_2018_06007_areawater.shp'); % this loads the water shapefile of Butte County, CA
cd ..
cd 'Airports'
Airport_shp = shaperead('airp_rw.shp'); % this loads the Airport shapefile of California
cd ..
% cd 'Fire_Stations'
% FireStation_shp = shaperead('fire_station_polygon.shp'); % this loads the water shapefile of Butte County, CA
% cd ..
% [lat,lon,Z,header,profile]=usgs24kdem('chico30m.dem',1);
% Z(Z==0) = -1;
% el1 = geoshow(lat,lon,Z,'DisplayType','surface');
% demcmap(Z)

%% Mapping 
LandBorders1=geoshow(gca,[Borders_shp.Y],[Borders_shp.X],'color',[0.3 0.3 0.3],'linewidth',0.25);
LandBorders3=geoshow(gca,[Water_shp.Y],[Water_shp.X],'color',[0.3 0.3 0.3],'linewidth',0.25);
geoshow(Borders_shp, 'FaceColor',[0.57 0.933 0.57])
geoshow(Water_shp, 'FaceColor',[0 0 1])
LandBorders2=geoshow(gca,[Roads_shp.Y],[Roads_shp.X],'color',[0.3 0.3 0.3],'linewidth',0.25);
LandBorders4=geoshow(gca,[Airport_shp.Y],[Airport_shp.X],'color',[1 0 1],'linewidth',2.50);
%LandBorders5=geoshow(gca,[FireStation_shp.Y],[FireStation_shp.X],'color',[1 0 1], 'linewidth',5.50);

% h=geoshow(gca, x,y,'DisplayType','multipoint');
% scatterm(x,y,[],z)
% % axesm('mercator',...
%     'FLatLimit',[39.763438, 39.939845],...
%     'FLonLimit',[-121.994719 -121.493366])
set(gca,'Xlim',[-121.974916 -121.474443],'YLim',[39.709120, 39.884156]) % sets limit on area of interest for analysis
xlabel('Lon')
ylabel('Lat')
