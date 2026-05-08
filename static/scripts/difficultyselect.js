let diffcultySelect = document.querySelector('.difficulty-select');
const form = document.querySelector('form');

diffcultySelect.addEventListener('click', (e) => {
    if (e.target.classList.contains('hard')) {
        form.action = '/game/new/' + e.target.id;
        if (document.getElementsByClassName('hard-info')[0].classList.contains('hide')) {
            document.getElementsByClassName('hard-info')[0].classList.remove('hide');
            if (!document.getElementsByClassName('normal-info')[0].classList.contains('hide')) {
                document.getElementsByClassName('normal-info')[0].classList.add('hide');
            }
        } else {
            document.getElementsByClassName('hard-info')[0].classList.add('hide');
        }
    }
    else if (e.target.classList.contains('normal')) {
        form.action = '/game/new'
        if (document.getElementsByClassName('normal-info')[0].classList.contains('hide')) {
            document.getElementsByClassName('normal-info')[0].classList.remove('hide');
            if (!document.getElementsByClassName('hard-info')[0].classList.contains('hide')) {
                document.getElementsByClassName('hard-info')[0].classList.add('hide');
            }
        } else {
            document.getElementsByClassName('normal-info')[0].classList.add('hide');
        }
    }
    else if (e.target.classList.contains('timed')) {
        form.action = '/game/new/timed_normal'
    }
})