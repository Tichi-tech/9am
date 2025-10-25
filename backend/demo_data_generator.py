"""
Demo Data Generator

Creates 4 weeks of journal entries showing realistic progression
to demonstrate the value of long-term trend analysis
"""
import json
import os
from datetime import datetime, timedelta

def generate_week1_entries():
    """Week 1: High anxiety, poor coping, isolation"""
    return [
        {
            "date": "2025-01-06",
            "time": "22:30",
            "text": "Can't sleep again. My mind won't shut off. Keep replaying that meeting where I stumbled over my words. Everyone probably thinks I'm incompetent. Why did I even speak up?"
        },
        {
            "date": "2025-01-07",
            "time": "08:15",
            "text": "Woke up with that familiar weight on my chest. Called in sick to work. I know I should push through but I just can't today. Spent the day in bed scrolling my phone."
        },
        {
            "date": "2025-01-08",
            "time": "19:45",
            "text": "Mom texted asking how I'm doing. Didn't respond. What would I even say? She wouldn't understand. Nobody does. Sometimes I feel like I'm screaming underwater."
        },
        {
            "date": "2025-01-09",
            "time": "23:00",
            "text": "Another panic attack at the grocery store. Had to abandon my cart and leave. The cashier was staring. I'm so embarrassed. Ordered delivery instead. Again."
        },
        {
            "date": "2025-01-10",
            "time": "14:30",
            "text": "Jake invited me to game night Friday. Made up an excuse. I know they're going to stop inviting me eventually. Maybe that's for the best. I'm just bringing everyone down anyway."
        },
        {
            "date": "2025-01-11",
            "time": "10:00",
            "text": "Therapy tomorrow. Part of me doesn't want to go. What's the point? We just talk in circles. But I promised myself I'd try. I guess that counts for something."
        },
        {
            "date": "2025-01-12",
            "time": "21:00",
            "text": "First therapy session focusing on anxiety. Therapist wants me to start journaling daily and try some breathing exercises. Feels pointless but I'll try. What do I have to lose?"
        }
    ]

def generate_week2_entries():
    """Week 2: Starting coping strategies, still struggling but small improvements"""
    return [
        {
            "date": "2025-01-13",
            "time": "22:00",
            "text": "Tried that breathing exercise today when I felt panic coming on. Didn't stop it but maybe it was less intense? Hard to tell. Still avoided the team lunch though."
        },
        {
            "date": "2025-01-14",
            "time": "09:30",
            "text": "Made it to work. Small victory. Used the breathing thing twice. Colleagues asked where I've been. Said I had a cold. The lying makes me feel worse but I can't explain the truth."
        },
        {
            "date": "2025-01-15",
            "time": "16:45",
            "text": "Actually went to the grocery store today. Heart was racing but I did the breathing exercise in the car first. Made it through checkout. Baby steps, I guess."
        },
        {
            "date": "2025-01-16",
            "time": "20:00",
            "text": "Called Mom back. Short conversation but it felt okay. She noticed I sounded better. I don't feel better but maybe I'm faking it better? Not sure if that's progress."
        },
        {
            "date": "2025-01-17",
            "time": "12:30",
            "text": "Panic attack during the morning standup. Had to step out. But I went BACK IN after calming down. Old me would have gone home. Therapist said to notice these small wins."
        },
        {
            "date": "2025-01-18",
            "time": "18:00",
            "text": "Weird realization: I've written in this journal every day this week. That's never happened before. Therapist was right that it helps to see patterns. I catastrophize everything."
        },
        {
            "date": "2025-01-19",
            "time": "22:30",
            "text": "Thinking about Jake's game night invitation. Still too scared to go but I miss them. Maybe next time I'll say yes. Maybe."
        }
    ]

def generate_week3_entries():
    """Week 3: Noticeable improvement, testing boundaries, some setbacks"""
    return [
        {
            "date": "2025-01-20",
            "time": "21:00",
            "text": "Had a good day. Is that allowed? I keep waiting for the other shoe to drop. Went for a walk at lunch instead of hiding at my desk. Co-worker Alex joined me."
        },
        {
            "date": "2025-01-21",
            "time": "10:15",
            "text": "Spoke up in the team meeting. Had a good idea about the project. People actually listened. Didn't spiral afterwards. This is new."
        },
        {
            "date": "2025-01-22",
            "time": "19:30",
            "text": "Jake texted again about plans. I said yes. SAID YES. Now I'm terrified but also excited? Is this what normal people feel? Therapy tomorrow - going to talk about this."
        },
        {
            "date": "2025-01-23",
            "time": "15:00",
            "text": "Rough day. Anxiety is back with a vengeance. Therapist reminded me progress isn't linear. I was doing so well. Why does it keep coming back? Frustrated with myself."
        },
        {
            "date": "2025-01-24",
            "time": "08:00",
            "text": "Woke up feeling heavy but I still got up. Did the breathing exercises. Made breakfast. These are things I couldn't do 2 weeks ago. Trying to remember that."
        },
        {
            "date": "2025-01-25",
            "time": "20:45",
            "text": "Game night was... okay. Left early because I was overwhelmed but I WENT. Jake was happy to see me. Nobody was mad I've been distant. Maybe I make up problems that don't exist?"
        },
        {
            "date": "2025-01-26",
            "time": "22:00",
            "text": "Looking back at my entries from week 1. I was in such a dark place. Still struggling but something has shifted. The panic attacks are less frequent. I'm trying. That has to count."
        }
    ]

def generate_week4_entries():
    """Week 4: Integration, building on progress, more good days than bad"""
    return [
        {
            "date": "2025-01-27",
            "time": "09:00",
            "text": "Monday morning and I'm not dreading it. When did that happen? Actually looking forward to the team lunch today. Planning to sit with Alex and the group."
        },
        {
            "date": "2025-01-28",
            "time": "18:30",
            "text": "Talked to Mom for an hour. Actually told her I've been struggling and seeing a therapist. She was supportive. Why did I think she wouldn't be? My anxiety lies to me."
        },
        {
            "date": "2025-01-29",
            "time": "14:00",
            "text": "Small setback today - felt panic rising during presentation prep. But I used my tools: breathing, grounding, talking to myself rationally. It passed. I didn't let it control me."
        },
        {
            "date": "2025-01-30",
            "time": "21:00",
            "text": "Therapy session was good. We talked about how I'm building a toolbox for anxiety instead of just white-knuckling through life. I can feel the difference."
        },
        {
            "date": "2025-01-31",
            "time": "16:45",
            "text": "Alex invited me to a concert next month. I said yes without the usual panic spiral. It's interesting - I still have anxiety but it doesn't run my life like it used to."
        },
        {
            "date": "2025-02-01",
            "time": "10:30",
            "text": "Went to the grocery store, bank, AND coffee shop today. Did errands like a normal person. A month ago this would have been impossible. Progress is real."
        },
        {
            "date": "2025-02-02",
            "time": "22:30",
            "text": "One month of therapy and journaling. I'm not 'cured' but I'm functional. I have hope. That's huge. The work is paying off. I'm proud of myself for sticking with it."
        }
    ]

def save_entries_to_json(entries, week_start, week_end, data_dir):
    """Save entries as individual daily files and weekly aggregate"""
    # Save daily files
    for entry in entries:
        filename = f"{entry['date']}.json"
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(entry, f, indent=2)

    # Save weekly aggregate
    weekly_data = {
        "patient_id": "demo_patient_001",
        "week_start": week_start,
        "week_end": week_end,
        "entries": entries
    }

    weekly_filename = f"week_{week_start}_to_{week_end}.json"
    weekly_filepath = os.path.join(data_dir, weekly_filename)
    with open(weekly_filepath, 'w') as f:
        json.dump(weekly_data, f, indent=2)

    print(f"✓ Saved {len(entries)} entries for week {week_start} to {week_end}")
    return weekly_filename

def main():
    """Generate all demo data"""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)

    print("Generating demo data for 4-week progression...\n")

    # Week 1: Jan 6-12
    week1 = generate_week1_entries()
    save_entries_to_json(week1, "2025-01-06", "2025-01-12", data_dir)

    # Week 2: Jan 13-19
    week2 = generate_week2_entries()
    save_entries_to_json(week2, "2025-01-13", "2025-01-19", data_dir)

    # Week 3: Jan 20-26
    week3 = generate_week3_entries()
    save_entries_to_json(week3, "2025-01-20", "2025-01-26", data_dir)

    # Week 4: Jan 27 - Feb 2
    week4 = generate_week4_entries()
    save_entries_to_json(week4, "2025-01-27", "2025-02-02", data_dir)

    print(f"\n✅ Demo data generated successfully!")
    print(f"📁 Location: {data_dir}")
    print(f"\n📊 Data shows progression from:")
    print(f"   Week 1: High anxiety, isolation, avoidance")
    print(f"   Week 2: Starting coping strategies, small wins")
    print(f"   Week 3: Testing boundaries, some setbacks")
    print(f"   Week 4: Integration, building on progress")
    print(f"\nUse this data to demonstrate long-term trend analysis!")

if __name__ == "__main__":
    main()
