cmake_minimum_required(VERSION 3.4)
project(dome)
add_subdirectory(pybind11)
pybind11_add_module(pyraspii rasp_master.cpp) 