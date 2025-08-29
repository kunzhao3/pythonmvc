from goods.entity.product import Product
from goods.libs.html import Html
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class products:
    def init(self):
        try:
          products = Product.get_all()
          logger.info(f"产品列表:{products}")
          return Html.render("/products.html", products=products)
        except Exception as e:
          logger.error(f"获取商品失败: {str(e)}")