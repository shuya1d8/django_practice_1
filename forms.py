import os
from django import forms
from .models import Blog, models
from django.core.mail import EmailMessage


class SexCoices(models.TextChoices):
    NO_ANS= '未選択', '未選択'
    MALE = '男', '男'
    FEMALE = '女', '女'
    OTHER_SEX = 'その他', 'その他'


class PostForm(forms.Form):
    post_email = forms.EmailField(label='メールアドレス')
    post_name = forms.CharField(label='お名前', max_length=30)
    post_sex = forms.ChoiceField(label='性別', choices=SexCoices.choices, required=False)
    post_title = forms.CharField(label='タイトル', max_length=30)
    post_contents = forms.CharField(label='内容', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""    #フォームのフィールドとラベルの間のコロンの非表示

        self.fields['post_email'].widget.attrs['class'] = 'form-control'
        self.fields['post_email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力してください。'

        self.fields['post_name'].widget.attrs['class'] = 'form-control'
        self.fields['post_name'].widget.attrs['placeholder'] = 'お名前をここに入力'

        self.fields['post_sex'].widget.attrs['class'] = 'form-control'
        self.fields['post_sex'].widget.attrs['style'] = 'width: 40%; '

        self.fields['post_title'].widget.attrs['class'] = 'form-control'
        self.fields['post_title'].widget.attrs['placeholder'] = 'タイトルを入力'

        self.fields['post_contents'].widget.attrs['class'] = 'form-control'
        self.fields['post_contents'].widget.attrs['placeholder'] = '内容を入力'

    def send_email(self):
        post_email = self.cleaned_data['post_email']
        post_name = self.cleaned_data['post_name']
        post_sex = self.cleaned_data['post_sex']
        post_title = self.cleaned_data['post_title']
        post_contents = self.cleaned_data['post_contents']

        subject = 'お問い合わせ {}'.format(post_title)
        message = 'メールアドレス： {0}\n送信者名： {1}\n性別：{2}\nメッセージ：{3}'.format(post_email, post_name, post_sex, post_contents)
        from_email = os.environ.get('FROM_EMAIL')
        to_list = [os.environ.get('FROM_EMAIL')]
        cc_list = [post_email]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
        message.send()


class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'photo1', 'photo2', 'photo3', 'release_flag')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
