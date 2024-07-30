document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('submitSolution').addEventListener('click', generateFeedback);
});

async function generateTask(context) {
    document.getElementById('loadingGifOutput').style.display = 'block';
    const response = await fetch('/generate-task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ context: context })
    });
    const result = await response.json();
    if (response.ok) {
        document.getElementById('aufgabenstellung').textContent = result.code;
    } else {
        console.error('Fehler beim Laden der Aufgabenstellung.');
    }
    document.getElementById('loadingGifOutput').style.display = 'none';
}

async function submitSolutionForOptimization() {
    const taskText = document.getElementById('aufgabenstellung').innerText;
    const studentSolution = document.getElementById('studentSolution').value;

    document.getElementById('loadingGifOutput').style.display = 'block';

    try {
        const response = await fetch('/optimierungsendpunkt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ taskText, studentSolution }),
        });

        if (!response.ok) {
            throw new Error('Netzwerkantwort war nicht ok.');
        }

        const data = await response.json();
        document.getElementById('optimierungsvorschlaege').innerText = data.optimierungsvorschlag;

    } catch (error) {
        console.error('Fehler beim Abrufen der Optimierungsvorschläge:', error);
    } finally {

        document.getElementById('loadingGifOutput').style.display = 'none';
    }
}

async function generateSampleSolution() {
    const taskText = document.getElementById('aufgabenstellung').innerText;

    document.getElementById('loadingGifOutput').style.display = 'block';

    try {
        const response = await fetch('/musterloesungsendpunkt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ taskText }),
        });

        if (!response.ok) {
            throw new Error('Netzwerkantwort war nicht ok.');
        }

        const data = await response.json();
        document.getElementById('musterloesung').innerText = data.musterloesung;

    } catch (error) {
        console.error('Fehler beim Abrufen der Musterlösung:', error);
    } finally {

        document.getElementById('loadingGifOutput').style.display = 'none';
    }
}

