import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


circuit = gpd.read_file("/content/spa_franchorchamps.geojson")

#re-word file to a projected Coordinated System
circuit_proj = circuit.to_crs(epsg=32633)


line = circuit_proj.geometry[0]
points = np.array(line.coords)

#calculation of sections
distance = 11
num_sections = len(points) // distance


colors = plt.cm.get_cmap('tab20', num_sections)

#plotting the map into different colors for different sections
fig, ax = plt.subplots(figsize=(8, 8))
for i in range(num_sections):
    start_index = i * distance
    end_index = min((i + 1) * distance, len(points))
    section_points = points[start_index:end_index]
    ax.plot(section_points[:, 0], section_points[:, 1], color=colors(i), linewidth=2)

ax.set_axis_off()
plt.savefig("circuit_colored_sections.png", dpi=300, bbox_inches='tight')
plt.close()

# image rotation
img = Image.open("circuit_colored_sections.png")
rotated_img = img.rotate(90, expand=True)
plt.imshow(rotated_img)
plt.axis('off')
plt.show()

# zoomed in images with boundaries
boundary_offset = 12
for i in range(num_sections):
    start_index = i * distance
    end_index = min((i + 1) * distance, len(points))
    section_points = points[start_index:end_index]

    #code so that lines dont overlap
    tangents = np.diff(section_points, axis=0)
    normals = np.array([-tangents[:, 1], tangents[:, 0]]).T
    norms = np.linalg.norm(normals, axis=1).reshape(-1, 1)
    normals = normals / norms

    normals = np.vstack([normals, normals[-1]])


    # create boundary lines
    left_boundary = section_points + boundary_offset * normals
    right_boundary = section_points - boundary_offset * normals

    # plot em
    fig, ax = plt.subplots(figsize=(8, 8))
    #ax.plot(section_points[:, 0], section_points[:, 1], color='black', linewidth=2)
    ax.plot(left_boundary[:, 0], left_boundary[:, 1], color='black', linewidth=2)
    ax.plot(right_boundary[:, 0], right_boundary[:, 1], color='black', linewidth=2)

    # zoomed in
    ax.set_xlim(min(section_points[:, 0]) - 10, max(section_points[:, 0]) + 10)
    ax.set_ylim(min(section_points[:, 1]) - 10, max(section_points[:, 1]) + 10)

    ax.set_axis_off()
    filename = f"circuit_section_{i}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

    # rotate and display each section image

    img = Image.open(filename)
    rotated_img = img.rotate(90, expand=True)
    plt.imshow(rotated_img)
    plt.axis('off')
    plt.show()

