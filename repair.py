import trimesh

def repair_stl(input_path, output_path):
    mesh = trimesh.load_mesh(input_path)

    mesh.remove_duplicate_faces()
    mesh.remove_degenerate_faces()
    mesh.remove_infinite_values()
    mesh.fill_holes()
    mesh.remove_unreferenced_vertices()

    mesh.export(output_path)

