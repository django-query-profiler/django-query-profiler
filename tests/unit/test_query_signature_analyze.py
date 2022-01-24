from unittest import TestCase

from django_query_profiler.query_profiler_storage import QuerySignature, QuerySignatureAnalyzeResult, StackTraceElement
from django_query_profiler.query_profiler_storage.django_stack_trace_analyze import _parse_sql_for_tables_and_eq


class QuerySignatureAnalyzeTest(TestCase):
    """ Contains Test cases from real django queries executed, with django_stack_trace """

    def test_filter_exists(self):
        query_without_params = '''
            SELECT (1) AS a FROM company_health_enrollment
            WHERE (company_health_enrollment.lineOfCoverage = %s AND company_health_enrollment.company_id = %s
                AND company_health_enrollment.isActive = %s AND company_health_enrollment.isEnrollmentComplete = %s)
            LIMIT 1
        '''

        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['company_health_enrollment'])
        self.assertEqual(where_equality_key, '')

        django_stack_trace = (StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
                              StackTraceElement('django.db.models.sql.compiler', 'has_results', None),
                              StackTraceElement('django.db.models.sql.query', 'has_results', None),
                              StackTraceElement('django.db.models.query', 'exists', None))

        query_signature: QuerySignature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.FILTER)

    def test_filter_first(self):
        query_without_params = '''
            SELECT employee_health_enrollment.id, employee_health_enrollment.employee_id,
                   employee_health_enrollment.createdAt, employee_health_enrollment.version_id,
                   employee_health_enrollment.premiumsMap, employee_health_enrollment.progress
            FROM employee_health_enrollment
            WHERE (employee_health_enrollment.employee_id = %s AND employee_health_enrollment.type = %s
                AND employee_health_enrollment.isActive = %s AND employee_health_enrollment.coverage_type = %s)
            ORDER BY employee_health_enrollment.id ASC LIMIT 1
        '''
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['employee_health_enrollment'])
        self.assertEqual(where_equality_key, '')

        django_stack_trace = [StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
                              StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
                              StackTraceElement('django.db.models.query', 'iterator', None),
                              StackTraceElement('django.db.models.query', '_fetch_all', None),
                              StackTraceElement('django.db.models.query', '__iter__', None),
                              StackTraceElement('django.db.models.query', '__getitem__', None),
                              StackTraceElement('django.db.models.query', 'first', None)]
        query_signature: QuerySignature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.FILTER)

    def test_filter(self):
        query_without_params = '''
            SELECT company_rate_version.id, company_rate_version.planId, company_rate_version.companyHealthEnrollmentId,
                   company_rate_version.companyId, company_rate_version.quoteParams
            FROM company_rate_version
            WHERE (company_rate_version.companyId IN (%s) AND company_rate_version.lineOfCoverage = %s
                  AND company_rate_version.planId IN (%s))
        '''
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['company_rate_version'])
        self.assertEqual(where_equality_key, '')

        django_stack_trace = [StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
                              StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
                              StackTraceElement('django.db.models.query', 'iterator', None),
                              StackTraceElement('django.db.models.query', '_fetch_all', None),
                              StackTraceElement('django.db.models.query', '__iter__', None)]
        query_signature: QuerySignature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.FILTER)

    def test_filter_with_join(self):
        query_without_params = '''
            SELECT (1) AS a
            FROM change_request
                INNER JOIN employment_type_change
                    ON ( change_request.employmentTypeChange_id = employment_type_change.id )
            WHERE (change_request.employee_id = %s AND change_request.isApplied = %s
                AND employment_type_change.employmentType = %s)
            LIMIT 1
        '''
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['change_request', 'employment_type_change'])
        self.assertEqual(where_equality_key, '')

        django_stack_trace = [StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
                              StackTraceElement('django.db.models.sql.compiler', 'has_results', None),
                              StackTraceElement('django.db.models.sql.query', 'has_results', None),
                              StackTraceElement('django.db.models.query', 'exists', None)]
        query_signature: QuerySignature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.FILTER)

    def test_get(self):
        query_without_params = '''
            SELECT register_company_employee.id, register_company_employee.version_id,
                   register_company_employee.user_id, register_company_employee.company_id,
                   register_company_employee.isHighlyCompensated, register_company_employee.middleInitial
            FROM register_company_employee
            WHERE register_company_employee.id = %s
            LIMIT 21
        '''
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['register_company_employee'])
        self.assertEqual(where_equality_key, 'register_company_employee.id')

        django_stack_trace = [StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
                              StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
                              StackTraceElement('django.db.models.query', 'iterator', None),
                              StackTraceElement('django.db.models.query', '_fetch_all', None),
                              StackTraceElement('django.db.models.query', '__len__', None),
                              StackTraceElement('django.db.models.query', 'get', None),
                              StackTraceElement('django.db.models.manager', 'manager_method', None)]
        query_signature: QuerySignature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.GET)

    def test_prefetch_related(self):
        query_without_params = '''
            SELECT employee_employment.id, employee_employment.version_id, employee_employment.isActive,
                   employee_employment.fullTimeStartDate_is_set, employee_employment.fullTimeEndDate_is_set
            FROM employee_employment
            WHERE employee_employment.employee_id = %s
        '''
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['employee_employment'])
        self.assertEqual(where_equality_key, 'employee_employment.employee_id')

        django_stack_trace = [StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
                              StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
                              StackTraceElement('django.db.models.query', 'iterator', None),
                              StackTraceElement('django.db.models.query', '_fetch_all', None),
                              StackTraceElement('django.db.models.query', '__iter__', None)]
        query_signature: QuerySignature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED)

    def test_select_related(self):
        query_without_params = '''
            SELECT employee_settings.id, employee_settings.employee_id, employee_settings.groupID,
                   employee_settings.dentalGroupID, employee_settings.visionGroupID,
                   employee_settings.dentalCompanyHealthCarrier_id_is_set
            FROM employee_settings
            WHERE employee_settings.employee_id = %s
        '''
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['employee_settings'])
        self.assertEqual(where_equality_key, 'employee_settings.employee_id')

        django_stack_trace = [StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
                              StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
                              StackTraceElement('django.db.models.query', 'iterator', None),
                              StackTraceElement('django.db.models.query', '_fetch_all', None),
                              StackTraceElement('django.db.models.query', '__len__', None),
                              StackTraceElement('django.db.models.query', 'get', None),
                              StackTraceElement('django.db.models.manager', 'manager_method', None),
                              StackTraceElement('django.db.models.fields.related_descriptors', 'get_object', None)]
        query_signature: QuerySignature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.MISSING_SELECT_RELATED)

    def test_prefetch_related_2(self):
        query_without_params = '''
            SELECT employee_health_enrollment.id, employee_health_enrollment.employee_id,
                    employee_health_enrollment.progress
             FROM employee_health_enrollment
             WHERE employee_health_enrollment.employee_id = %s
        '''
        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['employee_health_enrollment'])
        self.assertEqual(where_equality_key, 'employee_health_enrollment.employee_id')

        django_stack_trace = [StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
                              StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
                              StackTraceElement('django.db.models.query', 'iterator', None),
                              StackTraceElement('django.db.models.query', '_fetch_all', None),
                              StackTraceElement('django.db.models.query', '__iter__', None)]

        query_signature: QuerySignature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.MISSING_PREFETCH_RELATED)

    def test_select_related_2(self):
        query_without_params = '''
            SELECT carrier.id, carrier.carrierID, carrier.name, carrier.displayName, carrier.state,
                   carrier.newHireApprovalProcessingDays
            FROM carrier WHERE carrier.id = %s
            LIMIT 21
        '''

        table_names, _, where_equality_key = _parse_sql_for_tables_and_eq(query_without_params)
        self.assertListEqual(table_names, ['carrier'])
        self.assertEqual(where_equality_key, 'carrier.id')

        django_stack_trace = [StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
                              StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
                              StackTraceElement('django.db.models.query', 'iterator', None),
                              StackTraceElement('django.db.models.query', '_fetch_all', None),
                              StackTraceElement('django.db.models.query', '__len__', None),
                              StackTraceElement('django.db.models.query', 'get', None),
                              StackTraceElement('django.db.models.fields.related_descriptors', 'get_object', None)]
        query_signature: QuerySignature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.MISSING_SELECT_RELATED)

    def test_select_distinct_postgres(self):
        """
        This test validates SELECT DISTINCT ON that is allowable in Postgres
        See https://github.com/django-query-profiler/django-query-profiler/issues/21 for more details
        """

        query_without_params = '''
            SELECT DISTINCT ON (url) url, request_duration
            FROM logs
            ORDER BY url, timestamp DESC
        '''
        # self.assertRaises(ParseException, lambda: _parse_sql_for_tables_and_eq(query_without_params))

        django_stack_trace = [StackTraceElement('django.db.models.sql.compiler', 'execute_sql', None),
                              StackTraceElement('django.db.models.sql.compiler', 'results_iter', None),
                              StackTraceElement('django.db.models.query', 'iterator', None),
                              StackTraceElement('django.db.models.query', '_fetch_all', None),
                              StackTraceElement('django.db.models.query', '__iter__', None),
                              StackTraceElement('django.db.models.query', '__getitem__', None),
                              StackTraceElement('django.db.models.query', 'first', None)]
        query_signature: QuerySignature = QuerySignature(query_without_params, (), django_stack_trace, 'default')
        self.assertEqual(query_signature.analysis, QuerySignatureAnalyzeResult.UNKNOWN)
