import logging
from typing import Dict, List, Optional
from .product_selector import ProductSelector
from .revenue_optimizer import RevenueOptimizer

class CampaignManager:
    def __init__(self):
        self.campaigns = []
        self.product_selector = ProductSelector()
        self.revenue_optimizer = RevenueOptimizer()
        self.logger = logging.getLogger(__name__)

    def create_campaign(self, name: str, platform: str) -> str:
        """
        Creates a new affiliate marketing campaign.
        
        Args:
            name: Name of the campaign.
            platform: Platform where the campaign will be run (e.g., Facebook, Google).
            
        Returns:
            Campaign ID assigned to the newly created campaign.
        """
        try:
            campaign_id = f"cid_{len(self.campaigns) + 1}"
            self.campaigns.append({
                "id": campaign_id,
                "name": name,
                "platform": platform,
                "status": "active",
                "products": [],
                "tracking_links": {}
            })
            self.logger.info(f"Campaign '{name}' created with ID: {campaign_id}")
            return campaign_id
        except Exception as e:
            self.logger.error(f"Failed to create campaign '{name}': {str(e)}")
            raise

    def assign_product(self, campaign_id: str, product_ids: List[str]) -> None:
        """
        Assigns products to a specific campaign.
        
        Args:
            campaign_id: ID of the campaign to which products are assigned.
            product_ids: List of product IDs to be added to the campaign.
        """
        try:
            campaign = next((c for c in self.campaigns if c["id"] == campaign_id), None)
            if not campaign:
                raise ValueError(f"Campaign with ID '{campaign_id}' does not exist.")
            
            # Select high-performing products based on historical data
            selected_products = self.product_selector.select(products=product_ids)
            campaign["products"] = selected_products
            self.logger.info(f"Products assigned to campaign '{campaign['name']}': {selected_products}")
        except Exception as e:
            self.logger.error(f"Failed to assign products to campaign '{campaign_id}': {str(e)}")
            raise

    def generate_tracking_link(self, campaign_id: str, product_id: str) -> str:
        """
        Generates a unique tracking link for a specific product within a campaign.
        
        Args:
            campaign_id: ID of the campaign.
            product_id: ID of the product.
            
        Returns:
            Generated tracking link as a string.
        """
        try:
            # Ensure campaign and product exist
            campaign = next((c for c in self.campaigns if c["id"] == campaign_id), None)
            if not campaign:
                raise ValueError(f"Campaign with ID '{campaign_id}' does not exist.")
                
            product = next((p for p in campaign["products"] if p["id"] == product_id), None)
            if not product:
                raise ValueError(f"Product with ID '{product_id}' is not assigned to campaign '{campaign['name']}'.")
            
            # Generate unique tracking link
            tracking_link = f"{self._get_base_url(campaign['platform'])}/{product_id}_{len(campaign['tracking_links']) + 1}"
            campaign["tracking_links"][product_id] = tracking_link
            self.logger.info(f"Tracking link generated for product '{product_id}' in campaign '{campaign['name']}': {tracking_link}")
            return tracking_link
        except Exception as e:
            self.logger.error(f"Failed to generate tracking link: {str(e)}")
            raise

    def monitor_performance(self, campaign_id: str) -> Dict[str, float]:
        """
        Monitors and returns the performance metrics of a campaign.
        
        Args:
            campaign_id: ID of the campaign to monitor.
            
        Returns:
            Dictionary containing performance metrics (e.g., conversion rate, revenue).
        """
        try:
            campaign = next((c for c in self.campaigns if c["id"] == campaign_id), None)
            if not campaign:
                raise ValueError(f"Campaign with ID '{campaign_id}' does not exist.")
                
            # Assume metrics are fetched from a tracking system
            metrics = {
                "conversion_rate": 3.5,
                "revenue": 1234.56,
                "clicks": 1000,
                "impressions": 5000
            }
            self.logger.info(f"Performance metrics for campaign '{campaign['name']}: {metrics}")
            return metrics
        except Exception as e:
            self.logger.error(f"Failed to fetch performance metrics: {str(e)}")
            raise