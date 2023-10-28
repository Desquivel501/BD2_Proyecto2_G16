USE BD2;
GO

/*CONSULTAR NOMBRE LÓGICO DE LOS ARCHIVOS DE LOG*/
sp_helpdb BD2
GO

/*LEER CONTENIDO DEL ARCHIVO DE LOG*/
SELECT * FROM fn_dblog(null, null);
GO

/*OBTENER COLLATION DE LAS TABLAS*/
SELECT 
    t.name AS Tabla,
    c.name AS Columna,
    c.collation_name AS Collation_name
FROM sys.columns c
INNER JOIN sys.tables t
ON t.object_id = c.object_id;
GO

/*FRAGMENTACIÓN DE LOS ÍNDICES*/
SELECT 
    OBJECT_NAME(i.OBJECT_ID) AS 'Nombre',
    i.name AS 'índice',
   	ips.index_type_desc,
	ips.avg_fragmentation_in_percent 'Fragmentación (%)',
	ips.avg_page_space_used_in_percent 'Espacio de páginas usado (%)',
	ips.page_count 'Conteo de páginas (%)'
FROM sys.dm_db_index_physical_stats (DB_ID(), NULL, NULL, NULL, 'SAMPLED') ips
INNER JOIN sys.indexes i 
ON ips.OBJECT_ID = i.OBJECT_ID 
AND ips.index_id = i.index_id;
GO

/*REALIZANDO BACKUP DEL LOG
Backup log BD2
to disk  =‘C:\test\BackupLog.bak’
*/

/*CAMBIANDO A MODELO DE RECUPERACIÓN SIMPLE*/
ALTER DATABASE BD2
SET RECOVERY SIMPLE;
GO

/*REDUCIENDO LOG DE TRANSACCIONES A 1MB*/
DBCC SHRINKFILE(BD2_log, 1);
GO

/*CAMBIANDO A MODELO DE RECUPERACIÓN COMPLETO NUEVAMENTE*/
ALTER DATABASE BD2
SET RECOVERY FULL;
GO