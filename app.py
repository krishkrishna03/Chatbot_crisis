from flask import Flask, render_template, request, redirect, url_for
from nltk.chat.util import Chat, reflections
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['chatbot_db']
collection = db['ch']

# Define pairs of patterns and responses for the chatbot
pairs = [
    # Greetings
    (r'hello|hi|hey|good morning|good afternoon|good evening', ['Hello!', 'Hi there!', 'Hey!', 'Good morning!', 'Good afternoon!', 'Good evening!']),
    (r'how are you\??', ['I am just a computer program, but thanks for asking!']),
    (r'what\'s up\??', ['Not much, just here to assist you!']),
    (r'howdy\??', ['Howdy!']),
    (r'what\'s going on\??', ['Not much, just here to help!']),
    
    # Common Questions
    (r'what is your name\??', ['My name is ChatBot.']),
    (r'who created you\??', ['I was created by OpenAI.']),
    (r'what is the meaning of life\??', ['The meaning of life is a philosophical question that varies depending on individual beliefs and perspectives.']),
    (r'what is the capital of France\??', ['The capital of France is Paris.']),
    (r'what is the population of the world\??', ['The world population is approximately 7.9 billion people.']),
    (r'what is machine learning\??', ['Machine learning is a field of artificial intelligence that enables computers to learn from data and improve their performance on a task without being explicitly programmed.']),
    (r'what is artificial intelligence\??', ['Artificial intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems.']),
    (r'what is the internet\??', ['The internet is a global network of interconnected computers that allows for the exchange of information and communication between users around the world.']),
    (r'what is a computer\??', ['A computer is an electronic device that can perform various tasks by executing instructions given to it in the form of programs or software.']),
    
    # Environmental Topics
    (r'what is biodiversity loss\??', ['Biodiversity loss refers to the decline in the variety of living organisms in a particular ecosystem.']),
    (r'what is habitat destruction\??', ['Habitat destruction is the process by which natural habitats are damaged, degraded, or eliminated, leading to the loss of biodiversity and ecosystem services.']),
    (r'what is pollution\??', ['Pollution is the introduction of harmful substances or contaminants into the environment, which can cause adverse effects on ecosystems, human health, and the economy.']),
    (r'what is climate change\??', ['Climate change refers to long-term shifts in global or regional climate patterns, often attributed to human activities such as burning fossil fuels, deforestation, and industrial processes.']),
    (r'how do environmental crises impact ecosystems\??', ['Environmental crises can disrupt ecosystems by causing habitat loss, species extinction, altered food webs, and disrupted nutrient cycles.']),
    (r'how do environmental crises impact human health\??', ['Environmental crises can affect human health through air and water pollution, exposure to toxins, infectious diseases, food insecurity, and displacement from natural disasters.']),
    (r'how do environmental crises impact the economy\??', ['Environmental crises can result in economic losses due to damage to infrastructure, loss of ecosystem services, decreased agricultural productivity, increased healthcare costs, and reduced tourism revenues.']),
    (r'what are some examples of biodiversity loss\??', ['Examples of biodiversity loss include habitat destruction, overexploitation of natural resources, pollution, climate change, and invasive species introduction.']),
    (r'how can we mitigate habitat destruction\??', ['Habitat destruction can be mitigated through measures such as habitat restoration, protected area management, sustainable land use planning, and conservation efforts targeting key species and ecosystems.']),
    (r'what are the different types of pollution\??', ['The main types of pollution include air pollution (from industrial emissions, transportation, and burning fossil fuels), water pollution (from industrial discharges, agricultural runoff, and sewage), soil pollution (from chemical contaminants and waste disposal), and noise pollution.']),
    (r'what are the causes of climate change\??', ['The primary causes of climate change are human activities such as burning fossil fuels (coal, oil, and natural gas), deforestation, industrial processes, agriculture (livestock farming and rice paddies), and land use changes.']),
    (r'how can individuals contribute to mitigating environmental crises\??', ['Individuals can contribute to mitigating environmental crises by reducing their carbon footprint (using public transportation, conserving energy, and reducing waste), supporting sustainable practices (buying eco-friendly products, recycling, and conserving water), and advocating for environmental protection policies.']),
    (r'what are the consequences of ignoring environmental crises\??', ['Ignoring environmental crises can lead to irreversible damage to ecosystems, loss of biodiversity, increased frequency and severity of natural disasters, public health risks, economic losses, and social instability.']),
    (r'what are the key goals of environmental conservation\??', ['The key goals of environmental conservation include preserving biodiversity, protecting natural habitats and ecosystems, promoting sustainable use of natural resources, mitigating climate change, and ensuring environmental justice and equity.']),
    
    # Additional Environmental Questions
    (r'what is deforestation\??', ['Deforestation is the clearing of forests on a large scale, often resulting in land conversion for agriculture, logging, or urban development.']),
    (r'what is ocean acidification\??', ['Ocean acidification is the ongoing decrease in the pH of Earth\'s oceans, caused by the uptake of carbon dioxide (CO2) from the atmosphere, leading to adverse effects on marine life and ecosystems.']),
    (r'what is overfishing\??', ['Overfishing is the removal of fish from a body of water at a rate that the species cannot replenish, leading to depletion of fish stocks and disruption of marine ecosystems.']),
    (r'what is renewable energy\??', ['Renewable energy is energy that is generated from natural resources such as sunlight, wind, rain, tides, and geothermal heat, which are naturally replenished and environmentally sustainable.']),
    (r'what is sustainable development\??', ['Sustainable development is development that meets the needs of the present without compromising the ability of future generations to meet their own needs, balancing economic growth, social equity, and environmental protection.']),
    (r'what is e-waste\??', ['E-waste, or electronic waste, refers to discarded electronic devices that are no longer wanted or functional, which can contain hazardous materials and pose environmental and health risks if not properly disposed of or recycled.']),
    
    # Additional Environmental Questions
    (r'what is desertification\??', ['Desertification is the process by which fertile land becomes desert, typically as a result of deforestation, drought, or inappropriate agriculture practices, leading to soil degradation and loss of biodiversity.']),
    (r'what is water scarcity\??', ['Water scarcity refers to the lack of sufficient available water resources to meet the demands of water usage within a region or population, leading to water stress, conflicts, and environmental degradation.']),
    (r'what is air quality\??', ['Air quality refers to the condition of the air in terms of the presence of pollutants, such as particulate matter, ozone, nitrogen dioxide, sulfur dioxide, carbon monoxide, and volatile organic compounds, which can affect human health, ecosystems, and climate.']),
    (r'what is reforestation\??', ['Reforestation is the process of replanting trees in deforested or degraded areas, with the aim of restoring forest cover, biodiversity, ecosystem services, and carbon sequestration capacity.']),
    (r'what is wildlife conservation\??', ['Wildlife conservation is the practice of protecting wild animals and their habitats from threats such as habitat destruction, poaching, pollution, climate change, and human encroachment, to prevent species extinction and preserve biodiversity.']),
]

# Create a Chatbot using NLTK's Chat class
chatbot = Chat(pairs, reflections)

@app.route("/")
def profile():
    return render_template("profile.html")

@app.route("/project")
def aruna():
    # Fetch chat history from MongoDB
    chat_history = collection.find()
    return render_template("chat.html", chat_history=chat_history)

@app.route("/submit_message", methods=["POST"])
def submit_message():
    user_input = request.form["user_input"]
    bot_response = chatbot.respond(user_input)
    
    # Save the question and answer to MongoDB
    collection.insert_one({'user_input': user_input, 'bot_response': bot_response})

    # Redirect to the homepage to avoid resubmission of the form on page refresh
    return redirect(url_for("aruna"))

@app.route("/faqs")
def faqs():
    return render_template("faqs.html")

@app.route("/des")
def des():
    return render_template("des.html", nlp_info="Natural Language Processing (NLP) is a branch of artificial intelligence (AI) that focuses on the interaction between computers and humans through natural language.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
