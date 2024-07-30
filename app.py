#python 3.11.7 (base: conda)

# Abhängigkeiten/Bibliotheken, die benötigt werden
import os
import logging
from flask import Flask, request, jsonify, render_template
import openai
from flask_cors import CORS
import webbrowser
from threading import Timer
import random   

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/') # Aufruf der Seite von backend, kommt aus der flask
def home(): #
    return render_template('index.html') 
    return "Das Backend ist betriebsbereit!"

# Beginn Fallbeispiel
@app.route('/generate-task', methods=['POST'])
def generate_task():
    global letzte_Aufgabenstellung
    global fragestellung
    global obersatz
    global definition
    global loesung 
    global aufbau

    try:
        data = request.get_json()
        context = data['context']

        texte = [
            "Art. 2 Abs. 1: Jeder hat das Recht auf die freie Entfaltung seiner Persönlichkeit, soweit er nicht die Rechte anderer verletzt und nicht gegen die verfassungsmäßige Ordnung oder das Sittengesetz verstößt.",
            "Art. 3 Abs. 1: Alle Menschen sind vor dem Gesetz gleich.",
            "Art. 3 Abs. 2: Männer und Frauen sind gleichberechtigt. Der Staat fördert die tatsächliche Durchsetzung der Gleichberechtigung von Frauen und Männern und wirkt auf die Beseitigung bestehender Nachteile hin.",
            "Art. 4 Abs. 1: Die Freiheit des Glaubens, des Gewissens und die Freiheit des religiösen und weltanschaulichen Bekenntnisses sind unverletzlich.",
            "Art. 5 Abs. 1: Jeder hat das Recht, seine Meinung in Wort, Schrift und Bild frei zu äußern und zu verbreiten und sich aus allgemein zugänglichen Quellen ungehindert zu unterrichten. Die Pressefreiheit und die Freiheit der Berichterstattung durch Rundfunk und Film werden gewährleistet. Eine Zensur findet nicht statt.",
            "Art. 6 Abs. 1: Ehe und Familie stehen unter dem besonderen Schutze der staatlichen Ordnung.",
            "Art. 8 Abs. 1: Alle Deutschen haben das Recht, sich ohne Anmeldung oder Erlaubnis friedlich und ohne Waffen zu versammeln.",
            "Art. 9 Abs. 1: Alle Deutschen haben das Recht, Vereine und Gesellschaften zu bilden.",
            "Art. 10 Abs. 1: Das Briefgeheimnis sowie das Post- und Fernmeldegeheimnis sind unverletzlich.",
            "Art. 11 Abs. 1: Alle Deutschen genießen Freizügigkeit im ganzen Bundesgebiet.",
            "Art. 12 Abs. 1: Alle Deutschen haben das Recht, Beruf, Arbeitsplatz und Ausbildungsstätte frei zu wählen. Die Berufsausübung kann durch Gesetz oder auf Grund eines Gesetzes geregelt werden.",
            "Art. 13 Abs. 1: Die Wohnung ist unverletzlich.",
            "Art. 14 Abs. 1: Das Eigentum und das Erbrecht werden gewährleistet. Inhalt und Schranken werden durch die Gesetze bestimmt."
        ]

        text = random.choice (texte) # zufälliger Artikel wird ausgesucht

        # individuelle Lücke 
        if context == 'Schutzbereich':
            fragestellung = "Die Fragestellung soll das Format: Ist der Schutzbereich des Artikels eröffent (konkreter Artikel) haben"
            obersatz = "Der Obersatz lautet immer: Fraglich ist, ob der Schutzbereich eröffnet ist."
            definition = "Definiere im persönlichen Schutzbereich wen das Grundrecht schützt und im sachlichen Schutzbereich welches Verhalten geschützt wird."
            aufbau = "Zuerst immer den persönlichen und dann den sachlichen Schutzbereich prüfen. Aufbauschema 1. Schutzbereich a. persönlicher Schutzbereich b. sachlicher Schutzbereich"
            loesung = "Gebe nur die Lösung zum Schutzbereich aus"
        if context == 'Eingriff':
            fragestellung = "Die Fragestellung hat das Format: Ist ein Eingriff in den jeweiligen Artikel (konkreter Artikel) gegeben"
            obersatz = "Der Obersatz lautet immer: Fraglich ist, ob ein Eingriff in den jeweiligen Artikel (konkreter Artikel) gegeben ist"
            definition = "Der klassische Eingriff ist eine hoheitliche Maßnahme, die grundrechtlich gewährliestete Freiheit zielgerichtet, unmittelbar, rechtsförmig und zwingend mindert. Nach dem modernen Eingriffsbegriff ist jedes der öffentlichen Gewalt zurechnbare Handeln, das dem Grundrechtsträger ein grundrechtlich gewährleistetes Verhalten ganz oder teilwese unmöglich macht."
            aufbau = "Gehe  immer zuerst auf den klassischen Eingriffbegriff ein und dann auf den modernen Eingriffsbegriff. Aufbauschema 1. Eingriff a. klassicher Eingriff b. moderner Eingriff"
            loesung = "Gebe nur die Lösung zum Eingriff aus"
        if context == 'Rechtfertigung':
            fragestellung = "Die Fragestellung soll das Format: Ist der Eingriff verhältnismäßig (konkreter Artikel) haben"
            obersatz = "Der Obersatz lautet immer: Fraglich ist, ob der Eingriff verhältnismäßig ist."
            definition = " Legitimer Zweck = Der Zweck der Maßnahme ist legitim, wenn er auf das Wohl der Allgemeinheit gerichtet oder wenn für den Zweck eine staatlicher Schutzauftrab besteht. Geeignetheit = Geeignet ist eine Maßnahme, welche die Zweckerreichung zumindest fördert, Erfoderlichkeit = Erfoderlichkeit bedeutet, dass es kein gleich wirksames, aber milderes Mittel gibt, also das relatriv mildeste Mittel gewählt wurde, Angemessenheit = Die Maßnahme ist angemessen, wenn die Zweck-Mittel-Relation nicht außer verhältnis steht"
            aufbau = "Prüfe in der Rechtfertigung nur die Verhältnismäßigkeit mit dem Aufbau 1. legitimer Zweck 2. Geeignetheit 3. Erforderlichkeit 4. Angemessenheit)"
            loesung = "Gebe nur die Lösung zur Rechtfertigung aus."
    
        # Frage an openai wird gesendet
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Du bist an der juristitschen Universität Professor am Lehrstuhl öffentliches Recht und liest die Vorlesung Grundrechte in Bayern. In der Vorlesung über Grundrechte lehrt der Professor am Lehrstuhl für öffentliches Recht den Studierenden die Begründetheit der Verfassungsbeschwerde vor dem Bundesverfassungsgericht gemäß Art. 93 I Nr. 4a des Grundgesetzes. Die Begründetheit der Verfassungsbeschwerde hat den Aufbau 1.Schutzbereich 2. Eingriff 3. Rechtfertigung. Die Studenten sollen durch kurze Fallbeipsiel den juristischen Gutachtenstil erlernen."},
                {"role": "user", "content": f"Erstelle für die Studenten ein Fallbeispiel zu den Grundrechten. Frage den {text} ab. Gebe nur das Fallbeispiel aus. Das Fallbeispiel soll nur ein Problem zum Schutzbereich, Eingriff oder Rechtfertigung enthalten. Die Fragestellung des Falls soll am Ende sein. Stelle nur eine Frage. Beachte bei der Fragestellung die {fragestellung}  "}
            ]
        )

        generated_text = response.choices[0].message.content # generiertes Fallbeipsiel wird geladen
        # print(f"Generierte Aufgabenstellung: {generated_text}") #terminalausgabe
        letzte_Aufgabenstellung = generated_text
    except Exception as e: # Fehlerbehebung, um Errormessage zu bekommen im Terminal
        print(f"Fehler bei der Generierung: {e}") 
        return jsonify({"error": str(e)}), 500
    return jsonify({'code': generated_text})

def estimate_tokens(text):
    return len(text.split())


# Beginn Musterlösung
@app.route('/musterloesungsendpunkt', methods=['POST'])
def sample_solution_endpoint():
    try:
        data = request.json
        task_text = data['taskText'] # tast_text ist die Aufgabenstellung
        print(letzte_Aufgabenstellung)
        # Musterlösung Anfrage
        response_musterloesung = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du bist an der juristischen Universität Professor am Lehrstuhl öffentliches Recht und liest die Vorlesung Grundrechte in Bayern. In der Vorlesung über Grundrechte lehrt der Professor am Lehrstuhl für öffentliches Recht den Studierenden die Begründetheit der Verfassungsbeschwerde vor dem Bundesverfassungsgericht gemäß Art. 93 I Nr. 4a des Grundgesetzes. Du erstellt zu deinen Aufgabenstellungen eine juristische Musterlösung im Gutachtenstil. Der Gutachtentil fängt immer mit einem Obersatz hat, danach folgt eine Definiton und dann eine Subsumtion. "},
                {"role": "user", "content": f"Aufgabenstellung:\n{task_text}\n\n Erstelle eine Musterlösung für die Aufgabenstellung. Gehe dabei ausfühlich auf alle in der Aufgabenstellung aufgeworfenen Probleme ein. Beachte beim Aufbau folgendes: {loesung} {obersatz} {definition}."}
            ]
        )

        musterloesung = response_musterloesung.choices[0].message.content
        return jsonify({'musterloesung': musterloesung})
    except Exception as e:
        print(f"Fehler bei der Generierung: {e}")
        return jsonify({"error": str(e)}), 500


# Beginn Verbesserungsvorschlag
@app.route('/optimierungsendpunkt', methods=['POST'])
def optimization_endpoint():
    try:
        data = request.json
        task_text = data['taskText']
        student_solution = data['studentSolution']

        response_optimierung = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du bist an der juristischen Universität Professor am Lehrstuhl öffentliches Recht und liest die Vorlesung Grundrechte in Bayern. In der Vorlesung über Grundrechte lehrt der Professor am Lehrstuhl für öffentliches Recht den Studierenden die Begründetheit der Verfassungsbeschwerde vor dem Bundesverfassungsgericht gemäß Art. 93 I Nr. 4a des Grundgesetzes. Erstelle zu den studentischen Lösungen Verbesserungsvorschläge."}, #pormpt für Muserlösung
                {"role": "user", "content": f"Aufgabenstellung:\n{task_text}\n\nDie Studentische Lösung ist:{student_solution}\n\n. Überprüfe in dem Verbesserungsvorschlag, ob die Studenten den Gutachten stil beachtet haben.Gebe strukturelle Vorschläge und inhaltliche Vorschläge an."}
            ]
        )

        optimierungsvorschlag = response_optimierung.choices[0].message.content
        return jsonify({'optimierungsvorschlag': optimierungsvorschlag})
    except Exception as e:
        print(f"Fehler bei der Generierung: {e}")
        print(f"Optimierungsvorschlag: {optimierungsvorschlag}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
