#! /usr/bin/python

import os
import IPython
import hfts_grasp_planner.sdf.core as sdf_module
import hfts_grasp_planner.sdf.kinbody as kinbody_sdf_module
# import hfts_grasp_planner.sdf.robot as robot_sdf_module
# import hfts_grasp_planner.sdf.costs as costs_module
import openravepy as orpy
import numpy as np
import hfts_grasp_planner.placement.placement_planning as pp_module

ENV_PATH = '/home/joshua/projects/placement_planning/src/hfts_grasp_planner/data/environments/cluttered_env.xml'
SDF_PATH = '//home/joshua/projects/placement_planning/src/hfts_grasp_planner/data/sdfs/cluttered_test_env.sdf'
# ROBOT_BALL_PATH = '/home/joshua/projects/grasping_catkin/src/hfts_grasp_planner/models/r850_robotiq/ball_description.yaml'

def draw_volume(env, volume):
    return env.drawbox(0.5 * (volume[0] + volume[1]), 0.5 * (volume[1] - volume[0]), np.array([0.3, 0.3, 0.3, 0.3]))

def execute_placement_planner(placement_planner, body):
    best_node, best_val = placement_planner.sample(3)
    print 'Best val is ', best_val
    body.SetTransform(best_node.get_representative_value())

if __name__=="__main__":
    env = orpy.Environment()
    env.Load(ENV_PATH)
    env.SetViewer('qtcoin')
    robot_name = env.GetRobots()[0].GetName()
    scene_sdf = sdf_module.SceneSDF(env, [], excluded_bodies=[robot_name, 'bunny', 'crayola'])
    if os.path.exists(SDF_PATH):
        scene_sdf.load(SDF_PATH)
    else:
        # volume = np.array([-1.3, -1.3, -0.5, 1.3, 1.3, 1.2])
        # volume = (np.array([-0.35, 0.55, 0.64]), np.array([0.53, 0.9, 0.75]))
        volume = (np.array([-0.6, 0.3, 0.5]), np.array([0.7, 1.2, 1.0]))
        # volume = (np.array([-1.3, -1.3, -0.5]), np.array([1.3, 1.3, 1.2]))
        handle = draw_volume(env, volume)
        resolution = 0.005
        print 'Check volume!'
        IPython.embed()
        scene_sdf.create_sdf(volume, resolution, resolution)
        scene_sdf.save(SDF_PATH)
    vis_volume = np.array([0.15, 0.48, 0.65, 0.35, 0.8, 0.8])
    placement_planner = pp_module.PlacementGoalPlanner(None, env, scene_sdf)
    # placement_volume = (np.array([-0.35, 0.55, 0.64]), np.array([0.53, 0.9, 0.75]))
    placement_volume = (np.array([0.24, 0.58, 0.73]), np.array([0.29, 0.8, 0.8]))  # volume in small gap
    placement_planner.set_placement_volume(placement_volume)
    placement_planner.set_object('stick')
    body = env.GetKinBody('stick')
    handle = draw_volume(env, placement_volume)
    print "Check the placement volume!", placement_volume
    IPython.embed()
    handle = None
    execute_placement_planner(placement_planner, body)
    IPython.embed()