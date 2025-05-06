import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog, Scrollbar, Listbox, END, Text, SINGLE

def recommend_recipe(ingredients, recipes):
    recommended_recipes = []
    for index, recipe in recipes.iterrows():
        recipe_ingredients = str(recipe['Ingredients']).lower().split(', ')
        for ingredient in ingredients:
            if any(ingredient.strip().lower() in recipe_ingredient for recipe_ingredient in recipe_ingredients):
                recommended_recipes.append(recipe)
                break
    return recommended_recipes

def refresh_recipes_list():
    recipe_listbox.delete(0, END)
    for index, recipe in recipes.iterrows():
        recipe_listbox.insert(END, recipe['Title'])
9
def recommend_action():
    ingredients = []
    while True:
        ingredient = simpledialog.askstring("Ingredient Input", "Enter an ingredient (or leave empty to finish):")
        if ingredient is None or ingredient.strip() == "":
            break
        ingredients.append(ingredient)

    if not ingredients:
        messagebox.showinfo("Info", "No ingredients entered.")
        return

    matches = recommend_recipe(ingredients, recipes)

    if matches:
        recommended_listbox.delete(0, END)
        for recipe in matches:
            recommended_listbox.insert(END, recipe['Title'])
    else:
        messagebox.showinfo("No Matches", "No recipes found for the given ingredients.")
        recommended_listbox.delete(0, END)

def view_instruction_action():
    # Check if selection is in the recommended listbox first
    selected_idx = recommended_listbox.curselection()
    if selected_idx:
        selected_recipe = recommended_listbox.get(selected_idx)
    else:
        # If nothing selected in recommended listbox, check the main recipe listbox
        selected_idx = recipe_listbox.curselection()
        if not selected_idx:
            messagebox.showwarning("Warning", "Please select a recipe to view instructions.")
            return
        selected_recipe = recipe_listbox.get(selected_idx)
    
    instruction = recipes.loc[recipes['Title'] == selected_recipe, 'Instructions'].values[0]
    instruction_text.delete('1.0', END)
    instruction_text.insert(END, instruction)

def view_ingredients_action():
    # Check if selection is in the recommended listbox first
    selected_idx = recommended_listbox.curselection()
    if selected_idx:
        selected_recipe = recommended_listbox.get(selected_idx)
    else:
        # If nothing selected in recommended listbox, check the main recipe listbox
        selected_idx = recipe_listbox.curselection()
        if not selected_idx:
            messagebox.showwarning("Warning", "Please select a recipe to view ingredients.")
            return
        selected_recipe = recipe_listbox.get(selected_idx)
    
    ingredients = recipes.loc[recipes['Title'] == selected_recipe, 'Ingredients'].values[0]
    messagebox.showinfo("Ingredients", f"Ingredients for {selected_recipe}:\n{ingredients}")

def add_recipe_action():
    title = simpledialog.askstring("Add Recipe", "Enter recipe title:")
    if not title:
        return
    ingredients = simpledialog.askstring("Add Recipe", "Enter ingredients (separated by commas):")
    if not ingredients:
        return
    instructions = simpledialog.askstring("Add Recipe", "Enter instructions:")
    if not instructions:
        return
    cleaned_ingredients = ingredients.lower().replace('\n', '').strip()

    new_recipe = pd.DataFrame({
        'Title': [title],
        'Ingredients': [ingredients],
        'Instructions': [instructions],
        'Cleaned_Ingredients': [cleaned_ingredients]
    })

    global recipes
    recipes = pd.concat([recipes, new_recipe], ignore_index=True)
    messagebox.showinfo("Success", f"Recipe '{title}' added successfully!")
    refresh_recipes_list()

def delete_recipe_action():
    selected_idx = recipe_listbox.curselection()
    if not selected_idx:
        messagebox.showwarning("Warning", "Select a recipe to delete.")
        return

    selected_title = recipe_listbox.get(selected_idx)

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{selected_title}'?")
    if confirm:
        global recipes
        recipes = recipes[recipes['Title'] != selected_title].reset_index(drop=True)
        messagebox.showinfo("Deleted", f"Recipe '{selected_title}' deleted successfully.")
        refresh_recipes_list()

def save_changes_action():
    recipes.to_csv('Recipes Dataset.csv', index=False)
    messagebox.showinfo("Saved", "Changes saved to 'Recipes Dataset.csv'.")

def exit_action():
    root.destroy()

def search_recipe_action():
    search_term = search_entry.get().strip().lower()  # Get the search term in lowercase
    
    if search_term:  # Only search if the search term is not empty
        # Fixed: Use proper boolean indexing with na=False
        matching_recipes = recipes[recipes['Title'].str.lower().str.contains(search_term, na=False)]
        
        recipe_listbox.delete(0, END)  # Clear the listbox before adding search results
        if not matching_recipes.empty:
            for index, recipe in matching_recipes.iterrows():
                recipe_listbox.insert(END, recipe['Title'])
        else:
            messagebox.showinfo("No Matches", "No recipes found for the search term.")
    else:
        messagebox.showinfo("Info", "Please enter a search term.")

# Helper function to display selected recipe from main list in the text area
def show_selected_recipe(event):
    selected_idx = recipe_listbox.curselection()
    if selected_idx:
        selected_recipe = recipe_listbox.get(selected_idx)
        # Clear recommendation listbox when using main listbox
        recommended_listbox.selection_clear(0, END)
        
        # Show the instructions in the text area
        instruction = recipes.loc[recipes['Title'] == selected_recipe, 'Instructions'].values[0]
        instruction_text.delete('1.0', END)
        instruction_text.insert(END, instruction)

# GUI Setup
root = tk.Tk()
root.title("Recipe Recommendation System")
root.geometry("1000x600")

# Frames
left_frame = tk.Frame(root)
left_frame.pack(side='left', padx=10, pady=10, fill='both')

right_frame = tk.Frame(root)
right_frame.pack(side='right', padx=10, pady=10, fill='both', expand=True)

# Recipe Listbox
tk.Label(left_frame, text="All Recipes").pack()
recipe_listbox = Listbox(left_frame, width=40, height=20, selectmode=SINGLE)
recipe_listbox.pack()
# Bind double-click event to show recipe details
recipe_listbox.bind('<Double-1>', show_selected_recipe)

scrollbar = Scrollbar(left_frame)
scrollbar.pack(side='right', fill='y')
recipe_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=recipe_listbox.yview)

# Search Box and Button
search_entry = tk.Entry(left_frame, width=30)
search_entry.pack(pady=5)
tk.Button(left_frame, text="Search Recipe", command=search_recipe_action).pack(pady=5)

# Buttons
tk.Button(left_frame, text="Recommend Recipes", command=recommend_action).pack(pady=5)
tk.Button(left_frame, text="Add New Recipe", command=add_recipe_action).pack(pady=5)
tk.Button(left_frame, text="Delete Recipe", command=delete_recipe_action).pack(pady=5)
tk.Button(left_frame, text="Save Changes", command=save_changes_action).pack(pady=5)
tk.Button(left_frame, text="Exit", command=exit_action).pack(pady=5)

# Recommendation Listbox
tk.Label(right_frame, text="Recommended Recipes").pack()
recommended_listbox = Listbox(right_frame, width=50, height=10, selectmode=SINGLE)
recommended_listbox.pack(pady=5)

tk.Button(right_frame, text="View Instructions", command=view_instruction_action).pack(pady=5)
tk.Button(right_frame, text="View Ingredients", command=view_ingredients_action).pack(pady=5)

instruction_text = Text(right_frame, wrap='word', height=15, width=60)
instruction_text.pack(pady=5)

# Load recipes
try:
    recipes = pd.read_csv(r"C:\Users\vijey\Downloads\Recipes Dataset.csv")
    refresh_recipes_list()
except Exception as e:
    messagebox.showerror("Error", f"Failed to load recipe database: {str(e)}")
    recipes = pd.DataFrame(columns=['Title', 'Ingredients', 'Instructions', 'Cleaned_Ingredients'])

# Run the app
root.mainloop()