from geopy.distance import geodesic  
from shapely.geometry import LineString, Point
from pyproj import Geod
import numpy 
import math
# Define a geodesic object
geod = Geod(ellps="sphere")
line_NorthBAvencoordin = [(-35.275707,149.129453), (-35.240601,149.137072)]
line_GungDrcoordin = [(-35.224321,149.121756), (-35.257097,149.089787)]
line_BartonHwycoordin= [(-35.240601,149.137072),(-35.224321,149.121756)]
line_ParkesWaycoordin= [(-35.257097,149.089787),(-35.275707,149.129453)]
line_NorthBAven=LineString(line_NorthBAvencoordin)
line_GungDr=LineString(line_GungDrcoordin)
line_BartonHwy=LineString(line_BartonHwycoordin)
line_ParkesWay=LineString(line_ParkesWaycoordin)

crashPoints= {
    "point234892_15": (-35.27438171, 149.1339523),
    "point231209_15": (-35.39159842, 149.1618047),
    "point231240_15": (-35.20581863, 149.0688988),
    "point231546_15": (-35.30881723, 149.1295612),
    "point231562_15": (-35.37718095,149.1131836),
    "point221639_15": (-35.32147837,149.0640095),
    "point221375_15": (-35.24015127,149.1376193),
    "point223849_15": (-35.24134176,149.1494598),
    "point221821_15": (-35.23266435,149.1251032),
    "point222603_15": (-35.23920022,149.0574149),
    "point220238_15": (-35.34545966,149.06315),
    "point234892_15": (-35.27438171,149.1339523),
    "point232986_16": (-35.23656526,149.0701561),
    "point230596_16": (-35.24468208,149.0410726),
    "point246942_16": (-35.28594211,149.128148),
    "point245246_16": (-35.17782266,149.1063809),
    "point242161_16": (-35.28926258,149.1411253),
    "point242245_16": (-35.30255811,149.1782677),
    "point242562_16": (-35.24879425,149.1423371),
    "point235422_16": (-35.29065047,149.1272686),
    "point252315_17": (-35.46047665,149.0992988),
    "point251851_17": (-35.24574913,149.1345759),
    "point250627_17": (-35.40839748,149.0821422),
    "point250401_17": (-35.26895466,149.1306742),
    "point271494_17": (-35.27542459,149.096827),
    "point269668_17": (-35.37809492,149.1696535),
    "point267575_17": (-35.24317501,149.0477503),
    "point267265_17": (-35.3483043,149.06877),
    "point239564_18": (-35.35012637,149.0706468),
    "point237398_18": (-35.27347736,149.1219691),
    "point238935_18": (-35.3419899,149.0669444),
    "point238509_18": (-35.2600206,149.095859),
    "point269152_18": (-35.2760467,149.1411386),
    "point269835_18": (-35.23364316,149.0873371),
    "point272532_18": (-35.31841833,149.3954681),
    "point271344_18": (-35.31773958,149.1892973),
    "point236853_19": (-35.32685616,149.04147),
    "point239410_19": (-35.22493295,149.1239074),
    "point236436_19": (-35.4236301,149.0787116),
    "point236532_19": (-35.27385151,149.1177916),
    "point235797_19": (-35.24335392,149.1100081),
    "point265102_19": (-35.32021143,149.0982123),
    "point264264_19": (-35.32010849,149.2088025),
    "point227956_20": (-35.39591927,149.1557668),
    "point229694_20": (-35.20143142,149.0949017),
    "point227307_20": (-35.34106368,149.1616043),
    "point228630_20": (-35.29866185,149.1782481),
    "point225860_20": (-35.33976411,149.1703174),
    "point135_21": (-35.33768572,149.176075),
    "point189_21": (-35.20068908,149.1480236),
    "point226689_21": (-35.26108034,149.1362937)
}
lenghtline1=geodesic(line_NorthBAvencoordin[1],line_NorthBAvencoordin[0]).km
lenghtline2=geodesic(line_GungDrcoordin[1],line_GungDrcoordin[0]).km
lenghtline3=geodesic(line_BartonHwycoordin[1],line_BartonHwycoordin[0]).km
lenghtline4=geodesic(line_ParkesWaycoordin[1],line_ParkesWaycoordin[0]).km
i1=0
i2=0
i3=0
i4=0
pointscoord= {name: Point(lon, lat) for name, (lat, lon) in crashPoints.items()}
for name, pt in pointscoord.items():
   pointsOnLine1 = line_NorthBAven.interpolate(line_NorthBAven.project(pt))        
   pointsOnLine2 = line_GungDr.interpolate(line_GungDr.project(pt))    
   pointsOnLine3 = line_BartonHwy.interpolate(line_BartonHwy.project(pt))   
   pointsOnLine4 = line_ParkesWay.interpolate(line_ParkesWay.project(pt))  
   result1 = geod.inv(pt.x, pt.y, pointsOnLine1.y, pointsOnLine1.x)
   result2=geod.inv(pt.x, pt.y, pointsOnLine2.y , pointsOnLine2.x)
   result3=geod.inv(pt.x, pt.y, pointsOnLine3.y, pointsOnLine3.x)
   result4=geod.inv(pt.x, pt.y, pointsOnLine4.y, pointsOnLine4.x)
   result1_km=result1[2]/1000
   result2_km=result2[2]/1000
   result3_km=result3[2]/1000
   result4_km=result4[2]/1000
   if(result1_km < 1):
    print(f"Distance between {name} and NorthBAvenue is: {result1_km:.1f} km")
    print("The lenght of the line NorthBAvenue Road is: ",lenghtline1)
    i1=i1+1
   if(result2_km < 1):
    print(f"Distance between {name} and GungDr is: {result2_km:.1f} km")
    print("The lenght of the line GungDr Road is: ",lenghtline2)
    i2=i2+1
   if(result3_km < 1):
    print(f"Distance between {name} and BartonHwy is: {result3_km:.1f} km")
    print("The lenght of the line BartonHwy Road is: ",lenghtline3) 
    i3=i3+1  
   if(result4_km < 1):
    print(f"Distance between {name} and ParkesWay is: {result4_km:.1f} km")
    print("The lenght of the line ParkesWay Road is: ",lenghtline4)
    i4=i4+1 

crashdensity_NorthBAvenue=i1 / lenghtline1
crashdensity_GungDr=i2 / lenghtline2
crashdensity_BartonHwy=i3 / lenghtline3
crashdensity_ParkesWay=i4 / lenghtline4
print(f"The crash density in road NorthBAvenue is: {crashdensity_NorthBAvenue:.1f}, and that of GungDr is: {crashdensity_GungDr:.1f}, and that of BartonHwy is: {crashdensity_BartonHwy:.1f}, and that of ParkesWay is: {crashdensity_ParkesWay:.1f}")
speedlimitroad1=math.exp(0.01*60)
speedlimitroad2=math.exp(0.01*90)
speedlimitroad3=math.exp(0.01*100)
speedlimitroad4=math.exp(0.01*80)
print(f"The speed limit of road 1 is: {speedlimitroad1:.1f} and the speed limit of road 2 is: {speedlimitroad2:.1f} and the speed limit of road 3 is: {speedlimitroad3:.1f} and the speed limit of road 4 is: {speedlimitroad4:.1f}")
crossingPenalty=[0,0.2,0.3,0.1]
missingFootPathPenalty=[0,0.2,0.3,0.1]
separationBonus=[-0.3,-0.1,0,-0.2]
riskfactorRoad1=crashdensity_NorthBAvenue + speedlimitroad1 + crossingPenalty[0] + missingFootPathPenalty[0] + separationBonus[0]
riskfactorRoad2=crashdensity_GungDr + speedlimitroad2 + crossingPenalty[1] + missingFootPathPenalty[1] + separationBonus[1]  
riskfactorRoad3=crashdensity_BartonHwy + speedlimitroad3 + crossingPenalty[2] + missingFootPathPenalty[2] + separationBonus[2]  
riskfactorRoad4=crashdensity_ParkesWay + speedlimitroad4 + crossingPenalty[3] + missingFootPathPenalty[3] + separationBonus[3]  
print(f"The risk factor of road 1 is : {riskfactorRoad1:.1f} and the risk factor of road 2 is: {riskfactorRoad2:.1f} and the risk factor of road 3 is: {riskfactorRoad3:.1f} and the risk factor of road 4 is: {riskfactorRoad4:.1f}")

