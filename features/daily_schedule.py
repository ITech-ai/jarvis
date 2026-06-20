import json

FILE_PATH = "features/schedul.json"


def _reindex_tasks(day_entry):
    for index, task in enumerate(day_entry["tasks"], start=1):
        task["id"] = index


def read_schedule(day):
    day_lower = day.lower().strip()

    with open(FILE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
 
    for day_entry in data["weekly_tasks"]:
        if day_entry["day"].lower() == day_lower:
            if not day_entry["tasks"]:
                return "No tasks"
            
            lines = []
            for task in day_entry["tasks"]:
                lines.append(f"id{task['id']} {task['title']} {task['priority']}")
            
            return "\n".join(lines)
            
    return None


def write_schedule(day, task_title, task_priority="Medium"):
    day_lower = day.lower().strip()

    with open(FILE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    found = False
    for day_entry in data["weekly_tasks"]:
        if day_entry["day"].lower() == day_lower:
            found = True
            
            for task in day_entry["tasks"]:
                if task["title"].lower().strip() == task_title.lower().strip():
                    return None

            new_task = {
                "id": 0,
                "title": task_title,
                "priority": task_priority,
                "completed": False
            }
            day_entry["tasks"].append(new_task)
            _reindex_tasks(day_entry)
            
            added_task = day_entry["tasks"][-1]
            result = f"id{added_task['id']} {added_task['title']} {added_task['priority']}"
            break

    if found:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return result
    
    return None


def delete_schedule(day, task_id=None, task_title=None):
    if task_id is None and task_title is None:
        return None

    day_lower = day.lower().strip()

    with open(FILE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    day_found = False
    task_removed = False
    result = None

    for day_entry in data["weekly_tasks"]:
        if day_entry["day"].lower() == day_lower:
            day_found = True
            
            for task in day_entry["tasks"]:
                if (task_id is not None and task["id"] == task_id) or \
                   (task_title is not None and task["title"].lower().strip() == task_title.lower().strip()):
                    
                    result = f"id{task['id']} {task['title']} {task['priority']}"
                    
                    day_entry["tasks"].remove(task)
                    task_removed = True
                    break
            
            if task_removed:
                _reindex_tasks(day_entry)
            break

    if day_found and task_removed:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return result
        
    return None
