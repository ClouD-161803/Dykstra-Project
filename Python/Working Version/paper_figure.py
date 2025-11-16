import numpy as np
from convex_projection_solver import (DykstraProjectionSolver as Dykstra,
                                       DykstraStallDetectionSolver as FastForward)
from visualiser import ResultExporter, ComparisonVisualiser


def run() -> None:
    N_box = np.array([
        [1., 0.],
        [-1., 0.],
        [0., 1.],
        [0., -1.]
    ])
    c_box = np.array([1., 1., 1., 1.])
    
    corner_count = 1
    
    N_line = np.array([[1/2, 1], [-1/2, -1]])
    c_line = np.array([1, -1])
    
    z = np.array([-4., 1.4])
    x_range = [-2.25, 0.5]
    y_range = [0.5, 2]
    delete_half_spaces = True
    
    max_iter: int = 50 + 1
    plot_activity: bool = True
    plot_quivers: bool = False
    
    A: np.ndarray = np.vstack([N_box, N_line])
    c: np.ndarray = np.hstack([c_box, c_line])
    
    solver1 = Dykstra(
        z, A, c, max_iter,
        track_error=True,
        plot_errors=plot_quivers,
        plot_active_halfspaces=plot_activity,
        delete_spaces=delete_half_spaces
    )
    
    solver2 = FastForward(
        z, A, c, max_iter,
        track_error=True,
        plot_errors=plot_quivers,
        plot_active_halfspaces=plot_activity,
        delete_spaces=delete_half_spaces
    )
    
    result1 = solver1.solve()
    result2 = solver2.solve()
    
    solver1_name = "Dykstra"
    solver2_name = "Fast Forward"
    
    output_dir = "./results"
    
    ResultExporter.export(
        result=result1,
        output_path=output_dir,
        solver_name=solver1_name,
        initial_point=z,
        N=A,
        c=c,
        max_iter=max_iter,
        track_error=True,
        plot_errors=plot_quivers,
        plot_active_halfspaces=plot_activity
    )
    
    ResultExporter.export(
        result=result2,
        output_path=output_dir,
        solver_name=solver2_name,
        initial_point=z,
        N=A,
        c=c,
        max_iter=max_iter,
        track_error=True,
        plot_errors=plot_quivers,
        plot_active_halfspaces=plot_activity
    )
    
    print(f"\nSolver 1 ({solver1_name}) projection: {result1.projection}")
    print(f"Solver 2 ({solver2_name}) projection: {result2.projection}")
    
    nc_pairs1 = [
        ("Box", "Greys", N_box, c_box),
        ("Line", "Greys", N_line, c_line)
    ]
    nc_pairs2 = [
        ("Box", "Greys", N_box, c_box),
        ("Line", "Greys", N_line, c_line)
    ]
    
    visualiser = ComparisonVisualiser(
        result1, result2, nc_pairs1, nc_pairs2,
        max_iter, x_range, y_range,
        solver1_name, solver2_name,
        z,
        display_result_index=0,
        display_halfspace_index=0
    )
    visualiser.visualise()


if __name__ == "__main__":
    run()

