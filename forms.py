from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember = BooleanField('Ghi nhớ đăng nhập')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Tên đăng nhập', validators=[DataRequired(), Length(min=3, max=80)])
    full_name = StringField('Họ và tên', validators=[DataRequired(), Length(max=120)])
    phone = StringField('Số điện thoại', validators=[Length(max=20)])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Xác nhận mật khẩu', validators=[DataRequired(), EqualTo('password')])
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email đã được sử dụng.')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Tên đăng nhập đã tồn tại.')

class CheckoutForm(FlaskForm):
    customer_name = StringField('Họ và tên', validators=[DataRequired(), Length(max=120)])
    customer_email = StringField('Email', validators=[DataRequired(), Email()])
    customer_phone = StringField('Số điện thoại', validators=[Length(max=20)])

class AccountForm(FlaskForm):
    title = StringField('Tiêu đề tài khoản', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Mô tả')
    category = SelectField('Thể loại', choices=[
        ('Premium', 'Premium'),
        ('VIP', 'VIP'),
        ('Standard', 'Standard'),
        ('Special', 'Special')
    ], validators=[DataRequired()])
    rank = SelectField('Rank', choices=[
        ('Cao', 'Cao'),
        ('Trung bình', 'Trung bình'),
        ('Thấp', 'Thấp'),
        ('Elite', 'Elite')
    ])
    price = FloatField('Giá (VNĐ)', validators=[DataRequired(), NumberRange(min=0)])
    account_username = StringField('Tên tài khoản game')
    account_password = StringField('Mật khẩu tài khoản game')
    internal_notes = TextAreaField('Ghi chú nội bộ')
    images = MultipleFileField('Hình ảnh tài khoản', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Chỉ chấp nhận file ảnh!')])

class PaymentSettingsForm(FlaskForm):
    bank_id = StringField('Mã ngân hàng (BIN)', validators=[DataRequired(), Length(max=20)])
    bank_name = StringField('Tên ngân hàng', validators=[DataRequired(), Length(max=100)])
    account_number = StringField('Số tài khoản', validators=[DataRequired(), Length(max=50)])
    account_name = StringField('Tên chủ tài khoản', validators=[DataRequired(), Length(max=200)])
    qr_template = SelectField('Mẫu QR', choices=[
        ('compact', 'Compact'),
        ('compact2', 'Compact 2'),
        ('qr_only', 'QR Only')
    ], default='compact')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Mật khẩu mới', validators=[
        DataRequired(),
        Length(min=6, message='Mật khẩu phải có ít nhất 6 ký tự')
    ])
    confirm_password = PasswordField('Xác nhận mật khẩu', validators=[
        DataRequired(),
        EqualTo('password', message='Mật khẩu không khớp')
    ])
