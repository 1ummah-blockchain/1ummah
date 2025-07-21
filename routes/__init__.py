from flask import Blueprint

from .auth import auth_bp
from .wallet_routes import wallet_bp
from .mine import mine_bp
from .kyc import kyc_bp
from .referral import referral_bp
from .send import send_bp
from .activity import activity_bp

# إنشاء بلوبرنت رئيسي لتجميع كل البلوبرنتس
routes_bp = Blueprint('routes', __name__)

# تسجيل جميع الـ blueprints في البلوبرنت الرئيسي
routes_bp.register_blueprint(auth_bp)
routes_bp.register_blueprint(wallet_bp)
routes_bp.register_blueprint(mine_bp)
routes_bp.register_blueprint(kyc_bp)
routes_bp.register_blueprint(referral_bp)
routes_bp.register_blueprint(send_bp)
routes_bp.register_blueprint(activity_bp)
