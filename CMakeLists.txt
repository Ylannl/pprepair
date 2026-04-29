# prepair
#
# Copyright © 2009-2022,
# Ken Arroyo Ohori    k.ohori@tudelft.nl
# Hugo Ledoux         h.ledoux@tudelft.nl
# Martijn Meijers     b.m.meijers@tudelft.nl
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

cmake_minimum_required(VERSION 3.18)

if(POLICY CMP0167)
  cmake_policy(SET CMP0167 NEW)
endif()

project( pprepair )

set( CMAKE_BUILD_TYPE "Release")

# CGAL
find_package( CGAL 6 REQUIRED )

# Boost
find_package( Boost 1.50.0 REQUIRED )
find_package( GDAL 3.0 )

# Creating entries for target: pprepair
# ############################

add_executable( pprepair  FaceInfo.cpp IOWorker.cpp PlanarPartition.cpp PolygonHandle.cpp pprepair.cpp )

set_property(TARGET pprepair PROPERTY CXX_STANDARD 17)

target_link_libraries(pprepair PRIVATE CGAL::CGAL ${GDAL_LIBRARY} ${Boost_LIBRARIES})

install(TARGETS pprepair DESTINATION bin)