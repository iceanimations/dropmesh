'''
Created on Mar 27, 2014

@author: qurban.ali
'''

import pymel.core as pc

def get_lowest(mesh):
    num_vertices = mesh.numVertices()
    vtx = mesh.vtx[0]
    y = vtx.getPosition(space='world').y
    lowest = vtx
    for num in range(num_vertices):
        try:
            if mesh.vtx[num+1].getPosition(space='world')[1] < y:
                lowest = mesh.vtx[num+1]
        except: pass
    print 'lowest y: ', lowest.getPosition(space='world').y
    return lowest

def get_target(plane, lowest):
    vtx_pos = lowest.getPosition()
    temp = pc.dt.Point([vtx_pos[0], vtx_pos[1] - 1, vtx_pos[2]])
    dif = vtx_pos - temp
    direction = dif.normal()
    intersect_info = plane.intersect(vtx_pos, direction, space='world')
    print 'direction: ', direction
    print intersect_info
    if intersect_info[0]:
        return intersect_info[1][0].y
        

def place_meshes(margin = 0):
    selected_meshes = pc.ls(sl=True, geometry=True, dag=True)
    plane = selected_meshes[0]
    other_meshes = selected_meshes[1:]
    
    for mesh in other_meshes:
        lowest = get_lowest(mesh)
        target = get_target(plane, lowest)
        dif = lowest.getPosition(space='world').y - target
        pc.move(mesh, -dif - margin, r = True, y=True)