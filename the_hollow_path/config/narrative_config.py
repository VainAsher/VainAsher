"""
Narrative configuration for The Hollow Path.
Contains all story text, dialogues, and memory fragments.
"""

# Content Warning Text
CONTENT_WARNING = """
⚠️ CONTENT WARNING

This game explores themes of:
- Depression and mental health struggles
- Loss and separation from loved ones
- Institutional bias and legal challenges
- Recovery and hope

Mental health resources:
- 988 Suicide & Crisis Lifeline (US): Call/Text 988
- Crisis Text Line: Text HOME to 741741
- International: findahelpline.com

Press ENTER to continue or ESC to exit
"""

# Save Point Messages by Region
SAVE_POINT_MESSAGES = {
    "the_depths": "Rest here. It's okay to be tired.",
    "courtroom_maze": "You're still standing. That matters.",
    "the_void": "The silence doesn't have to be forever.",
    "support_circle": "You're safe here. Stay as long as you need.",
    "the_garden": "Growth takes time. You're doing well.",
    "the_bridge": "Looking forward, together.",
    "the_watchtower": "You've come so far. Keep going."
}

# Ability Unlock Messages
ABILITY_MESSAGES = {
    "first_step": {
        "name": "First Step",
        "description": "The decision to seek help. The hardest jump to make.",
        "message": "You've taken the first step. It gets easier."
    },
    "wall_climb": {
        "name": "Persistence",
        "description": "Finding ways forward despite the walls.",
        "message": "Walls aren't forever. Keep climbing."
    },
    "double_jump": {
        "name": "Partnership",
        "description": "Someone lifting you higher than you could go alone.",
        "message": "Together, you can reach new heights."
    },
    "dash": {
        "name": "Resilience",
        "description": "Pushing through the hardest moments.",
        "message": "You're stronger than you know."
    },
    "shadow_dash": {
        "name": "Moving Through Pain",
        "description": "Passing through trauma without being trapped.",
        "message": "The pain doesn't define you. Keep moving."
    },
    "grapple": {
        "name": "Hope",
        "description": "Reaching for distant connections.",
        "message": "Even distant lights can be reached."
    },
    "down_smash": {
        "name": "Impact",
        "description": "Using your momentum to create change.",
        "message": "Your struggles have given you strength."
    }
}

# Memory Fragments (found in The Void)
MEMORY_FRAGMENTS = {
    "memory_0": {
        "title": "Birthday Card",
        "text": "Birthday card, age 4. Handprint in paint.\n'To Daddy, Love You'\nYour hands were so small."
    },
    "memory_1": {
        "title": "Park Day",
        "text": "Photo: Three of you at the park.\nBoth kids on the swing.\nYou were pushing. Everyone was laughing."
    },
    "memory_2": {
        "title": "Bedtime Story",
        "text": "The dragon book. You read it every night.\n'Again, Daddy!'\nYou never got tired of it."
    },
    "memory_3": {
        "title": "First Day of School",
        "text": "Backpack almost as big as her.\nShe turned and waved at the door.\nYou waved back until she couldn't see."
    },
    "memory_4": {
        "title": "Beach Trip",
        "text": "Building sandcastles together.\nThe tide came in.\nThey didn't mind. You'd build more tomorrow."
    },
    "memory_5": {
        "title": "Sick Day",
        "text": "He had a fever. Fell asleep on your chest.\nYou stayed still for three hours.\nDidn't mind at all."
    },
    "memory_6": {
        "title": "Dance Recital",
        "text": "Pink tutu. Nervous before going on.\nYou said she'd be amazing.\nShe was."
    },
    "memory_7": {
        "title": "Skateboard Lesson",
        "text": "Teaching him to balance.\nFell six times. Got up seven.\n'I've got you, buddy.'"
    },
    "memory_8": {
        "title": "Last Hug",
        "text": "Dropping them off.\nThey didn't know it was the last time.\nNeither did you."
    },
    "memory_9": {
        "title": "Court Order",
        "text": "Supervised visits only.\nThen just letters.\nThen nothing.\nBut you never stopped trying."
    }
}

# NPC Dialogues (Support Circle)
NPC_DIALOGUES = {
    "marcus": {
        "name": "Marcus",
        "background": "Lost his career",
        "dialogues": [
            "I was a surgeon. One mistake. Lost everything.",
            "But here, I'm just Marcus. That's enough.",
            "These meetings... they remind me I'm more than my worst day.",
            "You belong here. We all do."
        ]
    },
    "david": {
        "name": "David",
        "background": "Divorced, financial ruin",
        "dialogues": [
            "Thought money was strength. Learned that's not where it comes from.",
            "These guys taught me what actually matters.",
            "Lost the house. Kept my life. Good trade.",
            "You don't have to be okay. Just have to keep going."
        ]
    },
    "james": {
        "name": "James",
        "background": "Veteran, PTSD",
        "dialogues": [
            "Told myself I didn't need help for years.",
            "Nearly didn't make it. But I'm here now.",
            "Every week. Every single week. It helps.",
            "The first time is the hardest. You already did that."
        ]
    },
    "ahmed": {
        "name": "Ahmed",
        "background": "Lost custody",
        "dialogues": [
            "Haven't seen my daughter in three years.",
            "But I'm here, staying ready, for when she can choose.",
            "They told me to move on. I'm not moving on. I'm moving forward.",
            "One day, she'll understand I never stopped trying."
        ]
    },
    "oliver": {
        "name": "Oliver",
        "background": "Suicide attempt survivor",
        "dialogues": [
            "Tried to leave. Glad I failed.",
            "These meetings? They're why I stay.",
            "It's not about being strong. It's about being here.",
            "Tomorrow can be different. I'm proof of that."
        ]
    }
}

# Companion Introduction
COMPANION_INTRODUCTION = """
A small shape in the shadows.
Cautious at first.
Then curious.
Then beside you.

[Cat companion acquired]
Press C to call.
"""

# Wedding Scene
WEDDING_SCENE = [
    "The bridge stretches ahead.",
    "Sunset colors paint the sky.",
    "Two figures, side by side.",
    "",
    "'I promise to be here.'",
    "'Through the dark. Through the light.'",
    "'Together.'",
    "",
    "[Wedding Ring acquired]",
    "[Fast travel network expanded]"
]

# Ending Messages
ENDING_MESSAGES = {
    "beacon_path": {
        "title": "The Beacon Keeper",
        "text": [
            "You've placed lights in every shadow.",
            "The path that nearly broke you now guides others.",
            "You can't undo the past.",
            "But you can light the way forward.",
            "",
            "They'll find their way to you.",
            "When they're ready, you'll be here.",
            "",
            "THE END"
        ]
    },
    "archive_path": {
        "title": "The Archivist",
        "text": [
            "Every memory preserved.",
            "Every moment honored.",
            "The love doesn't fade.",
            "Even in silence, it remains.",
            "",
            "One day, they'll read these.",
            "They'll understand you never stopped.",
            "",
            "THE END"
        ]
    },
    "true_ending": {
        "title": "The Hollow Path",
        "text": [
            "The beacons burn bright across the world.",
            "The archives stand complete.",
            "Your journey, preserved for those who follow.",
            "",
            "You descended into darkness.",
            "You faced every demon.",
            "You found light in unexpected places.",
            "You learned to carry both grief and hope.",
            "",
            "The children you miss every day...",
            "They're growing up, somewhere.",
            "Maybe they wonder about you too.",
            "",
            "When the time comes,",
            "When they're ready to ask,",
            "You'll be here.",
            "",
            "Whole. Healed. Waiting.",
            "",
            "THE HOLLOW PATH - COMPLETE",
            "",
            "Thank you for playing."
        ]
    }
}
