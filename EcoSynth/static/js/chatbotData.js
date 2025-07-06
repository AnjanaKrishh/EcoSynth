const chatbotData = {
  welcomeMessage: "👋 Welcome to EcoSynth Support! How can I help you today?",

  greetings: [
    "Hi there! 👋 How can I help you with waste management today?",
    "Hello! Need info on recycling, hazardous waste, or eco-tips?",
    "Good morning! 🌞 Ask me anything about upcycling or disposal methods.",
    "Good afternoon! ☀️ Let’s talk about sustainable waste practices.",
    "Good evening! 🌆 Need help with electronic or hazardous waste?",
    "Good night! 🌙 Feel free to ask anything before you log off."
  ],

  commonQuestions: [
    { question: "What are the main types of waste?", answer: "The main types are biodegradable, recyclable, hazardous, e-waste, and biomedical waste." },
    { question: "What is biodegradable waste?", answer: "Biodegradable waste breaks down naturally, like food scraps, garden waste, and paper." },
    { question: "What is non-biodegradable waste?", answer: "Non-biodegradable waste doesn't decompose easily, like plastics, metals, and e-waste." },
    { question: "How to upcycle plastic bottles?", answer: "Turn them into planters, lamps, eco-bricks, bird feeders, or wall organizers." },
    { question: "How to upcycle old newspapers?", answer: "Use them for gift wrapping, seedling pots, paper mache crafts, or handmade paper." },
    { question: "What can I do with glass bottles?", answer: "Convert glass bottles into lamps, vases, drinking glasses, or wall art." },
    { question: "How to reuse old clothes?", answer: "Make tote bags, quilts, cleaning cloths, cushion covers, or soft toys." },
    { question: "Can I upcycle used tires?", answer: "Yes, into garden seats, tire swings, planters, or even coffee tables." },
    { question: "What to do with wooden pallets?", answer: "Create shelves, tables, planters, wall decor, or compost bins." },
    { question: "Can I upcycle old CDs?", answer: "Use them for mosaic art, coasters, reflective decor, or wind chimes." },
    { question: "How to dispose of expired medicines?", answer: "Return them to pharmacies or use designated disposal bins. Do not flush or trash them." },
    { question: "How to dispose of batteries?", answer: "Drop them at e-waste collection centers. Avoid throwing them in normal bins." },
    { question: "What to do with broken fluorescent lamps?", answer: "Handle carefully and dispose via authorized e-waste centers due to mercury content." },
    { question: "How to get rid of old paint or solvents?", answer: "Use local hazardous waste disposal centers. Do not pour down the drain." },
    { question: "How to handle chemical waste from households?", answer: "Store safely and use municipality-approved disposal services or collection drives." },
    { question: "What is biomedical waste?", answer: "It includes used masks, syringes, gloves, and must be disposed of using color-coded bins." },
    { question: "What is waste segregation?", answer: "Separating biodegradable, recyclable, and hazardous waste to ensure proper disposal." },
    { question: "What is composting?", answer: "It's the natural process of turning food and garden waste into nutrient-rich fertilizer." },
    { question: "What is the 3Rs principle?", answer: "Reduce, Reuse, Recycle — key practices to manage waste and protect the environment." },
    { question: "What is a zero waste lifestyle?", answer: "A lifestyle that avoids single-use products and reduces landfill waste through reuse and composting." },
    { question: "Why is plastic waste harmful?", answer: "It pollutes oceans, harms animals, and takes hundreds of years to decompose." },
    { question: "What are India’s waste management rules?", answer: "India follows Solid Waste Rules (2016), Plastic Waste Rules (2022), E-Waste Rules (2022), and others." },
    { question: "What is the Plastic Waste Management Rules 2022?", answer: "It bans certain single-use plastics and enforces Extended Producer Responsibility (EPR)." },
    { question: "What are E-Waste Rules 2022?", answer: "They require producers to recycle e-waste via authorized recyclers and ensure safe tracking." },
    { question: "What is the Basel Convention?", answer: "A global treaty that restricts the movement of hazardous waste across borders, especially to developing nations." },
    { question: "What is Extended Producer Responsibility?", answer: "It holds manufacturers accountable for the entire lifecycle of their product, including take-back and recycling." },
    { question: "How can I contact EcoSynth?", answer: "Email us at support@ecosynth.com or use the EcoSynth app for waste pickup requests." },

    // ✅ Added Factory Reset Questions:
    { question: "How to factory reset an Android phone?", answer: "Go to Settings → System → Reset Options → Erase all data (factory reset)." },
    { question: "How to factory reset an iPhone?", answer: "Go to Settings → General → Transfer or Reset iPhone → Erase All Content and Settings." },
    { question: "Why should I reset my phone before recycling?", answer: "Factory reset removes personal data and prevents misuse of your device." },
    { question: "What to do before factory reset?", answer: "Backup your data, sign out of accounts, remove SIM and SD cards." }
  ],

  fallbackResponses: [
    "I'm not sure I understand. Try asking about waste types or how to upcycle something.",
    "I didn’t catch that. Try asking about rules, batteries, or composting.",
    "Need help with disposal? Ask me about e-waste or government guidelines.",
    "You can ask me how to recycle or reuse common items!",
    "You can also contact our team at support@ecosynth.com."
  ]
};
