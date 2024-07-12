$(document).ready(function() {
    // 获取当前用户已有的工作组名和Group ID
    $.ajax({
        type: 'GET',
        url: '/get_groups',
        success: function(response) {
            addGroupButtons(response.group_names, response.group_ids);
        }
    });

    // 创建工作组按钮
    $('#createGroupForm').on('submit', function(e) {
        e.preventDefault();
        var group_name = $('#group_name').val();
        if (!group_name) 
            $('#emptyError_group_name').show();
        else {
            $('#emptyError_group_name').hide();
            $.ajax({
                type: 'POST',
                url: '/create_group',
                data: JSON.stringify({group_name: group_name}),
                contentType: 'application/json',
                success: function(response) {
                    console.log('Group name created:', group_name);
                    console.log('Group ID: ', response.group_id);
                    $('#createGroup').modal('hide');
                    addGroupButtons([group_name], [response.group_id]);
                }
            });
        }
    });

    // 加入工作组按纽
    $('#joinGroupForm').on('submit', function(e) {
        e.preventDefault();
        var user_id = $('#user_id').val();
        var group_id = $('#group_id').val();
        var isValid = true;

        if (!user_id) {
            $('#emptyError_user_id').show();
            isValid = false;
        } else $('#emptyError_user_id').hide();
        
        if (!group_id) {
            $('#emptyError_group_id').show();
            isValid = false;
        } else $('#emptyError_group_id').hide();

        // 检查非空之后，进行通信检查
        if (isValid) {
            $.ajax({
                type: 'POST',
                url: '/broadcast',
                data: JSON.stringify({user_id: user_id, group_id: group_id}),
                contentType: 'application/json',
                success: function(response) {
                    // console.log('Group name created:', group_name);
                    // console.log('Group ID: ', response.group_id);
                    console.log(response);
                    $('#joinGroup').modal('hide');
                    // addGroupButtons([group_name], [response.group_id]);
                }
            });
        }
    });
});

// 动态添加工作组按钮
function addGroupButtons(group_names, group_ids) {
    const buttonsGroup = document.getElementById('buttons-Group');
    for (let i = 0; i < group_names.length; i++) {
        const button = document.createElement('button');
        button.className = 'group-btn btn btn-outline-primary';
        button.textContent = `${group_names[i]}`;
        button.id = group_ids[i];
        button.addEventListener('click', () => {
            const document_box = document.getElementById('document_content');
            document_box.placeholder = "😍请再选择一个用户😘";
            document_box.value = "";
            
            // 显示group_id和group_name
            const groupInfo = document.getElementById('group-info');
            groupInfo.innerHTML = `<b>${group_names[i]}</b> Group ID: ${group_ids[i]}`;
            $.ajax({
                type: 'POST',
                url: '/get_users',
                data: JSON.stringify({group_id: group_ids[i]}),
                contentType: 'application/json',
                success: function(response) {
                    addUserButtons(group_ids[i], response.user_names, response.user_ids);
                }
            });

            // 高亮当前选中的按钮
            const allButtons = buttonsGroup.getElementsByClassName('group-btn');
            for (let btn of allButtons) {
                btn.classList.remove('active');
            }
            button.classList.add('active');
        });
        buttonsGroup.appendChild(button);
    }
}

// 动态添加工作组用户按钮
function addUserButtons(group_id, user_names, user_ids) {
    const buttonsUser = document.getElementById('buttons-User');
    // 清除上一个工作组的用户按钮
    while (buttonsUser.firstChild) {
        buttonsUser.removeChild(buttonsUser.firstChild);
    }
    for (let i = 0; i < user_names.length; i++) {
        const button = document.createElement('button');
        button.className = 'user-btn btn btn-outline-success';
        button.textContent = `${user_names[i]}`;
        button.id = user_ids[i];
        button.addEventListener('click', () => {
            // 显示当前用户的文档
            const textarea = document.getElementById('document_content');
            textarea.placeholder = "( •̀ ω •́ )✧请在此处编辑文档🥳";
            $.ajax({
                type: 'POST',
                url: '/get_document',
                data: JSON.stringify({group_id: group_id, user_id: user_ids[i]}),
                contentType: 'application/json',
                success: function(response) {
                    textarea.value = response.text;
                }
            });

            // 高亮当前选中的按钮
            const allButtons = buttonsUser.getElementsByClassName('user-btn');
            for (let btn of allButtons) {
                btn.classList.remove('active');
            }
            button.classList.add('active');

            // 提交按钮
            $('#document').off('submit').on('submit', function(e) {
                e.preventDefault();
                var text = $('#document_content').val();
                $.ajax({
                    type: 'POST',
                    url: '/document_submit',
                    data: JSON.stringify({group_id: group_id, user_id: user_ids[i], text: text}),
                    contentType: 'application/json',
                    success: function(response) {
                        console.log('Current version:', response.version);
                    }
                });
            });
        });
        buttonsUser.appendChild(button);
    }
}

function setAvatar() {
    alert("设置头像功能（没写）");
}

window.addEventListener('beforeunload', function (e) {
    navigator.sendBeacon('/shutdown');
});