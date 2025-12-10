import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

# Thread pool for async UI rendering
_thread_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="ui-renderer")


def _render_ui_sync(recommended_component, fields, configs, data):
    """Synchronous UI rendering function (runs in thread pool)"""
    try:
        print(f"[UI GENERATOR] Starting async render: {recommended_component}")
        
        # Extract axis fields
        x_axis_field = fields.get("x_axis", "x")
        y_axis_field = fields.get("y_axis", "y")
        
        # Create a clean config without axis field names (matplotlib doesn't understand them)   
        match recommended_component:
            case "bar_chart":
                plt.figure(figsize=(12, 6))
                plt.bar(data[x_axis_field], data[y_axis_field], **configs)
                plt.xlabel(x_axis_field)
                plt.ylabel(y_axis_field)
                plt.title("Bar Chart")
                plt.show()
                
            case "line_chart":
                plt.figure(figsize=(12, 6))
                plt.plot(data[x_axis_field], data[y_axis_field], **configs)
                plt.xlabel(x_axis_field)
                plt.ylabel(y_axis_field)
                plt.title("Line Chart")
                plt.show()
                
            case "heatmap":
                plt.figure(figsize=(10, 8))
                plt.imshow(data, **configs)
                plt.colorbar()
                plt.title("Heatmap")
                plt.show()
                
            case "table":
                plt.figure(figsize=(12, 6))
                fig, ax = plt.subplots()
                ax.axis('tight')
                ax.axis('off')
                ax.table(cellText=data.values, colLabels=data.columns, **configs)
                plt.title("Data Table")
                plt.show()
                
            case _:
                print(f"[UI GENERATOR] [WARNING] Unknown chart type: {recommended_component}")
                print(f"[UI GENERATOR] Defaulting to table view")
                plt.figure(figsize=(12, 6))
                fig, ax = plt.subplots()
                ax.axis('tight')
                ax.axis('off')
                ax.table(cellText=data.values, colLabels=data.columns)
                plt.title("Data Table")
                plt.show()
        
        print(f"[UI GENERATOR] ✓ Async render completed for: {recommended_component}")
        
    except Exception as e:
        print(f"[UI GENERATOR] [ERROR] Error during async rendering: {str(e)}")
        import traceback
        traceback.print_exc()


def generate_ui_async(recommended_component, fields, configs, data):
    """Generate UI asynchronously without blocking the main program
    
    This function submits the UI rendering to a thread pool and returns immediately.
    The main program can continue processing while the visualization renders in the background.
    
    Args:
        recommended_component: Type of chart ('bar_chart', 'line_chart', 'heatmap', 'table')
        fields: Dict with 'x_axis' and 'y_axis' field names
        configs: Matplotlib configuration parameters
        data: Data to visualize (DataFrame or array-like)
    
    Returns:
        Future object that can be used to check if rendering is complete
    """
    print(f"[UI GENERATOR] Submitting async render task: {recommended_component}")
    print(f"[UI GENERATOR] Fields: {fields}, Configs: {configs}")
    
    # Submit to thread pool and return immediately
    future = _thread_pool.submit(_render_ui_sync, recommended_component, fields, configs, data)
    print(f"[UI GENERATOR] ✓ Task submitted to thread pool (non-blocking)")
    
    return future

# Keep legacy synchronous function for backward compatibility
def generate_ui(recommended_component, fields, configs, data):
    """Generate UI synchronously (blocking - legacy)
    
    This is the original synchronous implementation.
    Use generate_ui_async() for non-blocking rendering.
    
    Args:
        recommended_component: Type of chart
        fields: Dict with field names
        configs: Matplotlib configuration
        data: Data to visualize
    """
    print(f"[UI GENERATOR] Generating UI component (SYNC/BLOCKING): {recommended_component}")
    print(f"[UI GENERATOR] Data to be visualized: {data}")
    
    _render_ui_sync(recommended_component, fields, configs, data)
      
    