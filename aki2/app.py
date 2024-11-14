from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'gyaniquest_secret_key'

# Questions and answers for the game
questions = {
    "animal_or_object_or_cartoon": {
        "question": "Is it an animal, an object, or a cartoon character?",
        "animal": "animal_start",
        "object": "object_start",
        "cartoon": "cartoon_start"
    },
    # Animal questions
    "animal_start": {
        "question": "Is it a mammal?",
        "yes": "mammal",
        "no": "non_mammal"
    },
    "mammal": {
        "question": "Is it a wild animal?",
        "yes": "wild_mammal",
        "no": "domestic_mammal"
    },
    "wild_mammal": {
        "question": "Is it a carnivore?",
        "yes": "wild_carnivore",
        "no": "wild_herbivore"
    },
    "wild_carnivore": {
        "question": "Is it a lion?",
        "yes": "lion",
        "no": "is_it_a_tiger"
    },
    "is_it_a_tiger": {
        "question": "Is it a tiger?",
        "yes": "tiger",
        "no": "wild_carnivore_other"
    },
    "wild_herbivore": {
        "question": "Is it a giraffe?",
        "yes": "giraffe",
        "no": "wild_herbivore_other"
    },
    "domestic_mammal": {
        "question": "Is it a pet?",
        "yes": "pet_mammal",
        "no": "farm_animal"
    },
    "pet_mammal": {
        "question": "Is it a dog?",
        "yes": "dog",
        "no": "pet_mammal_other"
    },
    "farm_animal": {
        "question": "Is it a cow?",
        "yes": "cow",
        "no": "farm_animal_other"
    },
    "non_mammal": {
        "question": "Is it a reptile?",
        "yes": "reptile",
        "no": "other_animal"
    },
    "reptile": {
        "question": "Is it a dinosaur?",
        "yes": "dinosaur",
        "no": "non_mammal_other"
    },
    "other_animal": {
        "question": "Is it a mouse?",
        "yes": "mouse",
        "no": "other_animal_other"
    },

    # Object questions
    "object_start": {
        "question": "Is it a household item?",
        "yes": "household_item",
        "no": "non_household_item"
    },
    "household_item": {
        "question": "Is it used in the kitchen?",
        "yes": "kitchen_item",
        "no": "other_household_item"
    },
    "kitchen_item": {
        "question": "Is it a cooking appliance?",
        "yes": "cooking_appliance",
        "no": "kitchen_non_appliance"
    },
    "non_household_item": {
        "question": "Is it a piece of stationery?",
        "yes": "stationery",
        "no": "other_non_household_item"
    },
    "stationery": {
        "question": "Is it a pen?",
        "yes": "pen",
        "no": "other_stationery"
    },
    "other_household_item": {
        "question": "Is it a chair?",
        "yes": "chair",
        "no": "other_household_item"
    },

    # Cartoon questions
    "cartoon_start": {
        "question": "Is it a character from a popular cartoon show?",
        "yes": "popular_cartoon",
        "no": "non_popular_cartoon"
    },
    "popular_cartoon": {
        "question": "Is it from a cartoon show for kids?",
        "yes": "kids_cartoon",
        "no": "adult_cartoon"
    },
    "kids_cartoon": {
        "question": "Is it a character from 'Chhota Bheem'?",
        "yes": "chhota_bheem",
        "no": "other_kids_cartoon"
    },
    "other_kids_cartoon": {
        "question": "Is it a character from Motu Patlu?",
        "yes": "motu",
        "no": "other_cartoon"
    }
}

# Results for each answer path
results = {
    # Animal results
    "lion": "It is a lion!",
    "giraffe": "It is a giraffe!",
    "dog": "It is a dog!",
    "cow": "It is a cow!",
    "tiger": "It is a tiger!",
    "dinosaur": "It is a dinosaur!",
    "mouse": "It is a mouse!",
    "wild_carnivore_other": "It is a wild carnivore animal.",
    "wild_herbivore_other": "It is a wild herbivore animal.",
    "pet_mammal_other": "It is a pet mammal.",
    "farm_animal_other": "It is a farm animal.",
    "non_mammal_other": "It is a non-mammal animal.",
    "other_animal_other": "It is another type of animal.",
    
    # Object results
    "pen": "It is a pen.",
    "pencil": "It is a pencil.",
    "chair": "It is a chair.",
    "board": "It is a board.",
    "sofa": "It is a sofa.",
    "bed": "It is a bed.",
    "tv": "It is a TV.",
    "mobile": "It is a mobile phone.",
    "earphone": "It is a pair of earphones.",
    "dress": "It is a dress.",
    "bottle": "It is a bottle.",
    "cooking_appliance": "It is a cooking appliance.",
    "kitchen_non_appliance": "It is a non-appliance item in the kitchen.",
    "non_household_item": "It is a non-household item.",
    "other_stationery": "It is another type of stationery.",
    "other_household_item": "It is another type of household item.",

    # Cartoon results
    "chhota_bheem": "It is Chhota Bheem!",
    "motu": "It is Motu from Motu Patlu!",
    "patlu": "It is Patlu from Motu Patlu!",
    "doremon": "It is Doraemon!",
    "nobita": "It is Nobita from Doraemon!",
    "shizuka": "It is Shizuka from Doraemon!",
    "gyan": "It is Gyan from Gyan's World!",
    "ninja_hatori": "It is Ninja Hattori!",
    "pokemon": "It is a Pokemon character!",
    "non_popular_cartoon": "It is a non-popular cartoon character.",
    "other_cartoon": "It is a cartoon character from a less known show."
}

@app.route('/')
def index():
    session.clear()  # Clear session on home page
    return render_template('index.html')

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        classification = request.form['classification']
        if classification == 'animal':
            session['current_question'] = 'animal_start'
        elif classification == 'object':
            session['current_question'] = 'object_start'
        elif classification == 'cartoon':
            session['current_question'] = 'cartoon_start'
        return redirect(url_for('question'))

    return render_template('classify.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        answer = request.form['answer']
        current = session.get('current_question')

        if not current:
            return redirect(url_for('index'))

        # Get the next step based on the answer
        if answer == "yes":
            next_step = questions[current].get("yes")
        else:
            next_step = questions[current].get("no")

        # Check if we've reached the final answer (in results)
        if next_step in results:
            return redirect(url_for('result', item=next_step))

        session['current_question'] = next_step
        return redirect(url_for('question'))

    current_question = session.get('current_question')
    if not current_question:
        return redirect(url_for('index'))

    question_text = questions[current_question]["question"]
    return render_template('question.html', question=question_text)

@app.route('/result/<item>')
def result(item):
    result_sentence = results[item]
    return render_template('result.html', result=result_sentence)

if __name__ == '__main__':
    app.run(debug=True)
