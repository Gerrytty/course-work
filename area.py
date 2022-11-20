class Area:
    def __init__(self, r1, r2, r3, r4, area_image):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.r4 = r4

        self.lower_trash = 0
        self.upper_trash = 0
        self.sigma = 0

        self.area_image = area_image

        self.choosen_point = None
        self.point_from_cluster1 = None
        self.point_from_cluster2 = None

        self.nearest_point_in_first_cluster = None
        self.nearest_point_in_second_cluster = None
