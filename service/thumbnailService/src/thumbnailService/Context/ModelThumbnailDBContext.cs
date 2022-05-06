using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;
using thumbnailService.Entities.Sql;

namespace thumbnailService.Context
{
    public partial class ModelThumbnailDBContext : DbContext
    {
        public ModelThumbnailDBContext()
        {
        }

        public ModelThumbnailDBContext(DbContextOptions<ModelThumbnailDBContext> options)
            : base(options)
        {
        }

        public virtual DbSet<Jobs> Jobs { get; set; } = null!;
        public virtual DbSet<Jobstatus> Jobstatus { get; set; } = null!;
        
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                var configuration = new ConfigurationBuilder()
                                   .SetBasePath(Directory.GetCurrentDirectory())
                                   .AddJsonFile("appsettings.json")
                                   .Build();

                optionsBuilder.UseNpgsql(configuration.GetConnectionString("PostgresDB"));
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Jobs>(entity =>
            {
                entity.ToTable("jobs");

                entity.HasIndex(e => e.Id, "jobs_id_uindex")
                    .IsUnique();

                entity.Property(e => e.Id)
                    .ValueGeneratedNever()
                    .HasColumnName("id");

                entity.Property(e => e.Modelid).HasColumnName("modelid");

                entity.Property(e => e.Name).HasColumnName("name");

                entity.Property(e => e.Statusid).HasColumnName("statusid");

                entity.HasOne(d => d.Status)
                    .WithMany(p => p.Jobs)
                    .HasForeignKey(d => d.Statusid)
                    .HasConstraintName("jobstatus_fk");
            });

            modelBuilder.Entity<Jobstatus>(entity =>
            {
                entity.ToTable("jobstatus");

                entity.HasIndex(e => e.Id, "jobstatus_id_uindex")
                    .IsUnique();

                entity.Property(e => e.Id)
                    .ValueGeneratedNever()
                    .HasColumnName("id");

                entity.Property(e => e.Name).HasColumnName("name");
            });

            OnModelCreatingPartial(modelBuilder);
        }

        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
    }
}
