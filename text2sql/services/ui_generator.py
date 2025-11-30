import matplotlib.pyplot as plt
    

def generate_ui(recommended_component, fields, configs, data):
    """Generate the UI component based on the given recommendation and data"""  
    print(f"[UI GENERATOR] Generating UI component: {recommended_component} with fields: {fields} and configs: {configs}")
    print(f"[UI GENERATOR] Data to be visualized: {data}")
    
    # Extract axis fields
    x_axis_field = fields.get("x_axis", "x")
    y_axis_field = fields.get("y_axis", "y")
    
    # Create a clean config without axis field names (matplotlib doesn't understand them)   
    match recommended_component:
        case "bar_chart":
            plt.bar(data[x_axis_field], data[y_axis_field], **configs)
            plt.xlabel(x_axis_field)
            plt.ylabel(y_axis_field)
            plt.title("Bar Chart")
            plt.show()
            
        case "line_chart":
            plt.plot(data[x_axis_field], data[y_axis_field], **configs)
            plt.xlabel(x_axis_field)
            plt.ylabel(y_axis_field)
            plt.title("Line Chart")
            plt.show()
            
        case "heatmap":
            plt.imshow(data, **configs)
            plt.colorbar()
            plt.title("Heatmap")
            plt.show()
            
        case "table":
            fig, ax = plt.subplots()
            ax.axis('tight')
            ax.axis('off')
            ax.table(cellText=data.values(), colLabels=data.columns, **configs)
            plt.title("Data Table")
            plt.show()
            
        case _:
            print(f"[UI GENERATOR] [WARNING] Unknown chart type: {recommended_component}")
            print(f"[UI GENERATOR] Defaulting to table view")
            fig, ax = plt.subplots()
            ax.axis('tight')
            ax.axis('off')
            ax.table(cellText=data.values(), colLabels=data.columns)
            plt.title("Data Table")
            plt.show()
      
    