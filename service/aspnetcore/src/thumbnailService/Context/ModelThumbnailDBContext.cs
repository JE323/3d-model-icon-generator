using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.Extensions.Configuration;
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

        public virtual DbSet<Jobs> Jobs { get; set; }
        public virtual DbSet<Jobstatus> Jobstatus { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
#warning To protect potentially sensitive information in your connection string, you should move it out of source code. You can avoid scaffolding the connection string by using the Name= syntax to read it from configuration - see https://go.microsoft.com/fwlink/?linkid=2131148. For more guidance on storing connection strings, see http://go.microsoft.com/fwlink/?LinkId=723263.
                optionsBuilder.UseNpgsql("Host=localhost;Port=5432;Database=database;Username=admin;Password=admin");
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

                entity.Property(e => e.Name)
                    .IsRequired()
                    .HasColumnName("name");

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
