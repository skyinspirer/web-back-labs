function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitleRu = document.createElement('td');
            let tdTitleOrig = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitleRu.innerText = films[i].title_ru;
            tdTitleOrig.innerText = films[i].title;
            tdYear.innerText = films[i].year;
            
            tdTitleOrig.style.fontStyle = 'italic';
            tdTitleOrig.style.color = '#666';

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.style.backgroundColor = '#28a745';
            editButton.style.color = 'white';
            editButton.style.border = 'none';
            editButton.style.padding = '5px 10px';
            editButton.style.borderRadius = '3px';
            editButton.style.cursor = 'pointer';
            editButton.style.margin = '0 5px';
            editButton.onclick = function() {
                editFilm(films[i].id);
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.style.backgroundColor = '#dc3545';
            delButton.style.color = 'white';
            delButton.style.border = 'none';
            delButton.style.padding = '5px 10px';
            delButton.style.borderRadius = '3px';
            delButton.style.cursor = 'pointer';
            delButton.style.margin = '0 5px';
            delButton.onclick = function() {
                deleteFilm(films[i].id, films[i].title_ru);
            };

            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitleRu);
            tr.append(tdTitleOrig);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    })
    .catch(function(error) {
        console.error('Ошибка при загрузке фильмов:', error);
    });
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {
        method: 'DELETE'
    })
    .then(function(response) {
        if (response.ok) {
            fillFilmList();
        } else {
            alert('Ошибка при удалении фильма');
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
        alert('Ошибка при удалении фильма');
    });
}

function showModal() {
    document.querySelector('.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    document.getElementById('description-error').innerText = '';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    }

    document.getElementById('description-error').innerText = '';

    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(response) {
        if (response.ok) {
            fillFilmList();
            hideModal();
            return null;
        }
        return response.json();
    })
    .then(function(data) {
        if (data && data.description) {
            document.getElementById('description-error').innerText = data.description;
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при сохранении фильма');
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function(response) {
        if (!response.ok) {
            throw new Error('Фильм не найден');
        }
        return response.json();
    })
    .then(function(film) {
        document.getElementById('id').value = film.id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        document.getElementById('description-error').innerText = '';
        showModal();
    })
    .catch(function(error) {
        console.error('Ошибка при загрузке фильма:', error);
        alert('Не удалось загрузить данные фильма');
    });
}


document.addEventListener('DOMContentLoaded', function() {
    fillFilmList();
});