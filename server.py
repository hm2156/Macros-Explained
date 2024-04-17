from flask import Flask
from flask import render_template,  redirect, url_for
from flask import Response, request, jsonify

app = Flask(__name__)

macros= [
  {
    "id": 1,
    "name": "Proteins",
    "summary": "Proteins are crucial for muscle repair and growth in bodybuilding. They provide the amino acids needed to rebuild muscle tissue that is damaged during intense workouts",
    "myth":"More protein is not always better. Excessive protein can be converted to glucose or fat if consumed in large quantities beyond what your body can use for muscle repair and growth.",
    "context":"Proteins should be balanced with carbohydrates and fats in your diet. Carbohydrates are needed for energy, and fats are vital for hormone production",
    "imp":"Proteins are the building blocks of muscle. When you lift weights, you create micro-tears in your muscle fibers. Protein helps repair these tears, which leads to muscle growth",
    "sources":"High-Quality Sources: Lean meats, poultry, fish, dairy products, eggs, and plant-based sources like beans and lentils. Supplements: Whey, casein, soy, pea, and rice protein powders.",
    "intake":"Recommendations for protein intake can vary, but a common guideline is 1.6-2.2 grams of protein per kilogram of body weight for those involved in intense training.",
    "image": "https://www.scienceforsport.com/wp-content/uploads/2020/08/Protein1-scaled.webp"
  },
  {
    "id": 2,
    "name": "Carbohydrates",
    "summary":"Carbohydrates are a key energy source for bodybuilders, fueling both high-intensity training and recovery.",
    "myth":"Carbohydrates do not make you fat by themselves. It's about the overall caloric intake and balance in your diet. Quality and timing are key for bodybuilders.",
    "context":"While carbs are essential, it's important to balance them with adequate protein for muscle repair and healthy fats for hormonal balance.",
    "imp":"Carbohydrates are the body's preferred energy source. They're stored as glycogen in muscles and the liver and are utilized during both anaerobic and aerobic exercises.",
    "sources":"Complex Carbs: Whole grains, vegetables, fruits, and legumes provide sustained energy.Simple Carbs: Fruits and certain vegetables (like carrots and beets) provide quicker energy, ideal for pre/post-workout.",
    "intake":" Recommendations can vary based on training intensity and goals, but a common guideline for bodybuilders is 4-7 grams of carbohydrates per kilogram of body weigh",
    "image": "https://medlineplus.gov/images/Carbohydrates_share.jpg"
  },
  {
    "id": 3,
    "name": "Fats",
    "summary":"Fats play a crucial role in overall health and bodybuilding by supporting metabolism, hormone production, and energy.",
    "myth":"Dietary fat is not directly related to body fat. Excess calories contribute to fat gain, not consuming fats per se.",
    "context":"Balance is key. Fats should complement your intake of proteins and carbohydrates, not replace them. Quality matters, and so does the type of fat consumed.",
    "imp":"Fats provide a concentrated source of energy, particularly important during longer or lower-intensity workouts.",
    "sources":"Healthy Fats: Avocados, nuts, seeds, olive oil, and fatty fish like salmon provide omega-3 fatty acids and monounsaturated fats. Moderate Sources: Animal fats, coconut oil, and dairy products are good in moderation and provide saturated fats, necessary in small amount",
    "intake":"A common recommendation for bodybuilders is to get about 20-35% of total daily calories from fats.",
    "image": "https://domf5oio6qrcr.cloudfront.net/medialibrary/7412/285f8582-c1c9-4d28-9174-7d77f34dd548.jpg"
  }
]
quiz_questions = [
  {
    "id": 1,
    "question": "How much protein is generally recommended per kilogram of body weight for those involved in intense bodybuilding training?",
    "options": ["0.8-1.0 g", "1.6 - 2.2 g", "3.0 - 3.5", "2.5 - 3.0"],
    "answer": "1.6 - 2.2 g"
  },
  {
    "id": 2,
    "question": "What is the primary role of carbohydrates in a bodybuilding diet?",
    "options": ["To enhance flavor in meals", "To provide a concentrated source of energy", "To serve as the body's preferred source of energy", "To promote fat storage for energy reserves"],
    "answer": "To serve as the body's preferred source of energy"
  },
  {
    "id": 3,
    "question": "Which types of fats are considered healthy and should be included in a bodybuilder's diet?",
    "options": ["Saturated fats from processed foods", "Trans fats from deep-fried foods", "Omega-3 fatty acids from sources like fatty fish and flaxseeds", "Only animal fats for hormone production"],
    "answer": "Omega-3 fatty acids from sources like fatty fish and flaxseeds"
  },
  {
    "id": 4,
    "question": "What is the role of dietary fats in relation to hormone production for bodybuilding?",
    "options": ["Dietary fats decrease hormone production and should be minimized.", "They have no impact on hormone production but are essential for flavor.", "Fats are necessary for the absorption of water-soluble vitamins like B and C.", "Fats are vital for the synthesis of hormones, including testosterone, which is essential for muscle growth."],
    "answer": "Fats are vital for the synthesis of hormones, including testosterone, which is essential for muscle growth."
  },
  {
    "id": 5,
    "question": "How do macronutrient needs typically change during the bulking and cutting phases of bodybuilding?",
    "options": ["During bulking, increase proteins and decrease carbohydrates and fats.", "In both phases, keep protein high; during bulking, increase carbohydrates and fats; during cutting, decrease carbohydrates and slightly reduce fats.", "During cutting, increase carbohydrates and fats to ensure energy for intense workouts.", "Macronutrient needs do not change; only caloric intake should be adjusted."],
    "answer": "In both phases, keep protein high; during bulking, increase carbohydrates and fats; during cutting, decrease carbohydrates and slightly reduce fats."
  }
]
user_answers = [None]*5

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/calc')
def calc():
    return render_template('calculate.html')

@app.route('/learn/<int:lesson_id>')
def learn(lesson_id):
    lesson_data = next((lesson for lesson in macros if int(lesson['id']) == lesson_id), None)

    if lesson_data is None:
       
        return "Lesson not found", 404

    return render_template('learn.html', lesson=lesson_data)


@app.route('/calculate-macros', methods=['GET', 'POST'])
def calculate_macros():
    if request.method == 'POST':
        gender = request.form.get('gender')
        weight = float(request.form.get('weight'))  # Weight in kilograms
        height = float(request.form.get('height'))  # Height in centimeters
        age = float(request.form.get('age'))  # Age in years
        activity = request.form.get('activity')  # Activity level

        # BMR Calculation using Mifflin-St Jeor Equation
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        # Activity Level Multiplier
        activity_levels = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        activity_multiplier = activity_levels.get(activity, 1.2)

        # Total Daily Energy Expenditure (TDEE)
        tdee = round(bmr * activity_multiplier)

        # Macronutrient distribution ratios
        protein_ratio = 0.3
        fat_ratio = 0.25
        carb_ratio = 0.45

        # Macros in grams
        protein = round((tdee * protein_ratio) / 4, 1)
        fat = round((tdee * fat_ratio) / 9, 1)
        carbs = round((tdee * carb_ratio) / 4, 1)

        # Adjustments for goal
        weight_loss_calories = round(tdee * 0.85)
        bulking_calories = round(tdee * 1.15)

        # Results dictionary
        results = {
            'maintenance': {
                'calories': tdee,
                'protein': protein,
                'carbs': carbs,
                'fats': fat
            },
            'weight_loss': {
                'calories': weight_loss_calories,
                'protein': protein, 
                'carbs': round(carbs * 0.85, 1),
                'fats': round(fat * 0.85, 1)
            },
            'bulking': {
                'calories': bulking_calories,
                'protein': protein,  
                'carbs': round(carbs * 1.15, 1),
                'fats': round(fat * 1.15, 1)
            }
        }

        return render_template('result.html', results=results)

    # GET request, show the form
    return render_template('calculate.html')


@app.route('/quiz/<int:question_id>', methods=['GET', 'POST'])
def quiz(question_id):
    global user_answers

    # Get the current question
    question = next((q for q in quiz_questions if q['id'] == question_id), None)

    if question is None:
        return "Question not found", 404

    if request.method == 'POST':
        # Store the user's answer
        user_answer = request.form.get('option')
        user_answers[question_id - 1] = user_answer

        # Check if this is the last question
        if question_id == len(quiz_questions):
            return redirect(url_for('quiz_result'))
        else:
            return redirect(url_for('quiz', question_id=question_id + 1))

    # Initialize the user_answers list if it's empty
    if not user_answers:
        user_answers = [None] * len(quiz_questions)

    # Render the question
    return render_template('quiz1.html', question=question, question_id=question_id, user_answer=user_answers[question_id - 1])

@app.route('/quiz_result')
def quiz_result():
	global user_answers

	# Calculate the score
	score = 0
	quiz_results = []
	print(user_answers)
	for i, user_answer in enumerate(user_answers):
			correct_answer = quiz_questions[i]['answer']
			is_correct = user_answer == correct_answer
			if is_correct:
					score += 1
			quiz_results.append({
					'question': quiz_questions[i]['question'],
					'user_answer': user_answer,
					'correct_answer': correct_answer,
					'is_correct': is_correct
			})

	return render_template('quiz_result.html', score=score, total_questions=len(quiz_questions), quiz_results=quiz_results)


if __name__ == '__main__':
    app.run(debug=True)
