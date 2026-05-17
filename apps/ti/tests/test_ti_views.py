from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import MagicMock, patch

User = get_user_model()


class TIViewsTestCase(TestCase):
    def setUp(self):
        self.ti_user = User.objects.create_user(
            username="ti_admin",
            password="password123",
            is_staff=True,
            is_superuser=True
        )

        # Setup patcher for mock_diag
        self.patcher = patch('apps.ti.views.diagnostico')
        self.mock_diag = self.patcher.start()
        self.mock_diag.get_system_resources.return_value = {'cpu_percent': 10, 'ram_percent': 20}
        self.mock_diag.get_db_stats.return_value = {'size': '10MB', 'tables': 50, 'vendor': 'sqlite'}
        self.mock_diag.get_git_info.return_value = {'git_hash': 'abcdef1'}
        self.mock_diag.check_external_integrations.return_value = []
        self.mock_diag.check_ssl_expiry.return_value = {'days_left': 30}
        self.mock_diag.get_topology_data.return_value = {}
        self.mock_diag.get_orphan_files_count.return_value = 0
        self.mock_diag.get_user_activity.return_value = {'sessoes_ativas': 5}
        self.mock_diag.get_request_stats.return_value = {'latencia_media': '50ms', 'taxa_erro': '0%'}
        self.mock_diag.get_security_health_score.return_value = 95
        self.mock_diag.get_disk_breakdown.return_value = {}
        self.mock_diag.get_slow_queries.return_value = []
        self.mock_diag.get_comm_health.return_value = {}
        self.mock_diag.get_task_queue_stats.return_value = {'pending': 0}
        self.mock_diag.get_backup_status.return_value = {'last_backup': 'Nunca', 'size': '0MB', 'location': 'N/A'}
        self.mock_diag.get_anomaly_status.return_value = {'status': 'OK', 'confidence': '100%', 'alerts_24h': 0}
        self.mock_diag.get_lgpd_stats.return_value = {'pending_requests': 0}
        self.mock_diag.get_security_audit_summary.return_value = {'2fa_adoption': '10%', 'weak_passwords': 0}
        self.mock_diag.get_performance_heatmap.return_value = []
        self.mock_diag.get_global_event_feed.return_value = []
        self.mock_diag.get_db_connections.return_value = 5
        self.mock_diag.get_cache_stats.return_value = {}

    def tearDown(self):
        self.patcher.stop()

    def test_painel_ti_access_mocked(self):
        self.client.force_login(self.ti_user)
        url = reverse('ti:painel')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"v7.2.4", response.content)

    def test_infraestrutura_ti_access_mocked(self):
        self.client.force_login(self.ti_user)
        url = reverse('ti:infraestrutura')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hub de", response.content)

    def test_api_logs_lgpd_mocked(self):
        self.client.force_login(self.ti_user)
        url = reverse('ti:api_lgpd_logs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')
