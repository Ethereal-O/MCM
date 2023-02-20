import random
import cv2
import imageio

class check:
    def isRayIntersectsSegment(poi,s_poi,e_poi):
        if s_poi[1]==e_poi[1]:
            return False
        if s_poi[1]>poi[1] and e_poi[1]>poi[1]:
            return False
        if s_poi[1]<poi[1] and e_poi[1]<poi[1]:
            return False
        if s_poi[1]==poi[1] and e_poi[1]>poi[1]:
            return False
        if e_poi[1]==poi[1] and s_poi[1]>poi[1]:
            return False
        if s_poi[0]<poi[0] and e_poi[1]<poi[1]:
            return False

        xseg=e_poi[0]-(e_poi[0]-s_poi[0])*(e_poi[1]-poi[1])/(e_poi[1]-s_poi[1])
        if xseg<poi[0]:
            return False
        return True
    
    def isPoiWithinPoly(poi,poly):
        sinsc=0
        for i in range(len(poly)-1): #[0,len-1]
            s_poi=poly[i]
            e_poi=poly[i+1]
            if check.isRayIntersectsSegment(poi,s_poi,e_poi):
                sinsc+=1
            

        return True if sinsc%2==1 else  False

class getMotion:
    poly_boader = [(39,299),(161,201),(257,285),(298,325),(310,450),(39,299)]
    poly_three_borders = [[(39,299),(161,201),(184,303),(165,371),(39,299)],[(161,201),(257,285),(310,450),(161,201)],[(257,285),(298,325),(310,450),(165,371),(184,303),(257,285)]]
    def get_motion(poi):
        if not check.isPoiWithinPoly(poi,getMotion.poly_boader):
            return [0,0]
        migrate_vec = getMotion.get_migrate_vector(poi)
        random_vec = getMotion.get_random_vector()
        tot_vec = [migrate_vec[0] + 5*random_vec[0], migrate_vec[1] + 5*random_vec[1]]
        return tot_vec
    
    def get_migrate_vector(poi):
        if check.isPoiWithinPoly(poi,getMotion.poly_three_borders[0]):
            return [2.63,-2.14]
        if check.isPoiWithinPoly(poi,getMotion.poly_three_borders[1]):
            return [0.34,2.75]
        if check.isPoiWithinPoly(poi,getMotion.poly_three_borders[2]):
            return [0.34,2.75]
        return [random.random(),random.random()]
    
    def get_random_vector():
        return [random.random(),random.random()]
        
class simulation:
    start = [92,315]
    def init():
        migration = [(int(simulation.start[0] + 10*random.random()),int(simulation.start[1] + 10*random.random())) for i in range(500)]
        return migration
    def update(ans):
        ans_up = []
        for an in ans:
            motion = getMotion.get_motion(an)
            ans_up.append((int(an[0]+8*motion[0]),int(an[1]+8*motion[1]))) 
        return ans_up

class drawPermanentData:
    def getAll(img):
        drawPermanentData.getElephant(img)
    def getElephant(img):
        elephant_circle_points = [(82,275),(161,241),(185,331),(260,380)]
        elephant_points = []
        for point in elephant_circle_points:
            for i in range(100):
                elephant_points.append((int(point[0]+70*random.random()),int(point[1]+70*random.random())))
        for point in elephant_points:
            cv2.circle(img,point,2,(255,0,0),-1)
        
def main():
    points = simulation.init()
    imgs=[]
    for i in range(1000):
        img = cv2.imread("./map_all.jpg") # 读取图片
        points = simulation.update(points)
        for point in points:
            cv2.circle(img,point,2,(0,0,255),-1)
            
        drawPermanentData.getAll(img)
        imgs.append(img)
        
    imageio.mimsave("test.gif",imgs,fps=1)
    
if __name__ == "__main__":
    main()